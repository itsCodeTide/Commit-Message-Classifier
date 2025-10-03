from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import re
from datetime import datetime
import uvicorn

app = FastAPI(title="Commit Message Classifier API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class CommitMessage(BaseModel):
    message: str

class ClassificationResult(BaseModel):
    message: str
    type: str
    scope: str | None
    description: str
    confidence: float
    timestamp: str
    suggestions: List[str]

class BatchCommitMessages(BaseModel):
    messages: List[str]

# Commit type patterns and descriptions
COMMIT_TYPES = {
    'feat': {
        'pattern': r'^feat(\([^)]+\))?:\s*.+',
        'description': 'A new feature',
        'keywords': ['add', 'new', 'implement', 'create', 'introduce']
    },
    'fix': {
        'pattern': r'^fix(\([^)]+\))?:\s*.+',
        'description': 'A bug fix',
        'keywords': ['fix', 'bug', 'resolve', 'correct', 'repair', 'patch']
    },
    'docs': {
        'pattern': r'^docs(\([^)]+\))?:\s*.+',
        'description': 'Documentation changes',
        'keywords': ['doc', 'documentation', 'readme', 'comment', 'guide']
    },
    'style': {
        'pattern': r'^style(\([^)]+\))?:\s*.+',
        'description': 'Code style changes (formatting, semicolons, etc.)',
        'keywords': ['style', 'format', 'indent', 'whitespace', 'lint']
    },
    'refactor': {
        'pattern': r'^refactor(\([^)]+\))?:\s*.+',
        'description': 'Code refactoring',
        'keywords': ['refactor', 'restructure', 'optimize', 'improve', 'clean']
    },
    'perf': {
        'pattern': r'^perf(\([^)]+\))?:\s*.+',
        'description': 'Performance improvements',
        'keywords': ['performance', 'perf', 'speed', 'optimize', 'faster']
    },
    'test': {
        'pattern': r'^test(\([^)]+\))?:\s*.+',
        'description': 'Adding or updating tests',
        'keywords': ['test', 'testing', 'spec', 'coverage', 'unit', 'integration']
    },
    'build': {
        'pattern': r'^build(\([^)]+\))?:\s*.+',
        'description': 'Build system or dependency changes',
        'keywords': ['build', 'dependency', 'deps', 'package', 'npm', 'pip']
    },
    'ci': {
        'pattern': r'^ci(\([^)]+\))?:\s*.+',
        'description': 'CI/CD configuration changes',
        'keywords': ['ci', 'cd', 'pipeline', 'jenkins', 'travis', 'github actions']
    },
    'chore': {
        'pattern': r'^chore(\([^)]+\))?:\s*.+',
        'description': 'Other changes that don\'t modify src or test files',
        'keywords': ['chore', 'update', 'upgrade', 'maintenance', 'config']
    },
    'revert': {
        'pattern': r'^revert(\([^)]+\))?:\s*.+',
        'description': 'Reverts a previous commit',
        'keywords': ['revert', 'undo', 'rollback']
    }
}

def extract_scope(message: str) -> str | None:
    """Extract scope from conventional commit format"""
    scope_match = re.search(r'\(([^)]+)\)', message)
    return scope_match.group(1) if scope_match else None

def calculate_confidence(message: str, commit_type: str) -> float:
    """Calculate confidence score for classification"""
    message_lower = message.lower()
    
    # Check if it matches the conventional format
    pattern = COMMIT_TYPES[commit_type]['pattern']
    if re.match(pattern, message, re.IGNORECASE):
        return 0.95
    
    # Check for keywords
    keywords = COMMIT_TYPES[commit_type]['keywords']
    keyword_matches = sum(1 for kw in keywords if kw in message_lower)
    
    if keyword_matches > 0:
        return min(0.6 + (keyword_matches * 0.1), 0.9)
    
    return 0.5

def classify_commit(message: str) -> Dict:
    """Classify a commit message"""
    message = message.strip()
    
    if not message:
        raise HTTPException(status_code=400, detail="Empty commit message")
    
    # First, try to match conventional commit format
    for commit_type, info in COMMIT_TYPES.items():
        if re.match(info['pattern'], message, re.IGNORECASE):
            scope = extract_scope(message)
            description = re.sub(r'^[^:]+:\s*', '', message)
            
            return {
                'type': commit_type,
                'scope': scope,
                'description': description,
                'confidence': 0.95
            }
    
    # If no conventional format, classify by keywords
    message_lower = message.lower()
    best_match = 'chore'
    best_confidence = 0.0
    
    for commit_type, info in COMMIT_TYPES.items():
        keywords = info['keywords']
        keyword_matches = sum(1 for kw in keywords if kw in message_lower)
        
        if keyword_matches > 0:
            confidence = calculate_confidence(message, commit_type)
            if confidence > best_confidence:
                best_confidence = confidence
                best_match = commit_type
    
    return {
        'type': best_match,
        'scope': None,
        'description': message,
        'confidence': max(best_confidence, 0.5)
    }

def generate_suggestions(message: str, classification: Dict) -> List[str]:
    """Generate suggestions to improve commit message"""
    suggestions = []
    commit_type = classification['type']
    
    # Check if follows conventional format
    if not re.match(COMMIT_TYPES[commit_type]['pattern'], message, re.IGNORECASE):
        suggestions.append(f"Consider using conventional format: {commit_type}: {classification['description']}")
    
    # Check message length
    if len(message) < 10:
        suggestions.append("Commit message is too short. Add more details.")
    
    if len(message) > 100:
        suggestions.append("Commit message is long. Consider keeping summary under 72 characters.")
    
    # Check for imperative mood
    first_word = classification['description'].split()[0].lower() if classification['description'] else ''
    past_tense_indicators = ['added', 'fixed', 'updated', 'changed', 'removed', 'created']
    if any(first_word.startswith(ind) for ind in past_tense_indicators):
        suggestions.append("Use imperative mood (e.g., 'add' instead of 'added')")
    
    # Check capitalization
    desc = classification['description']
    if desc and desc[0].isupper():
        suggestions.append("Start description with lowercase letter")
    
    return suggestions

@app.get("/")
def read_root():
    return {
        "message": "Commit Message Classifier API",
        "version": "1.0.0",
        "endpoints": {
            "/classify": "POST - Classify a single commit message",
            "/classify/batch": "POST - Classify multiple commit messages",
            "/types": "GET - Get all commit types and their descriptions"
        }
    }

@app.post("/classify", response_model=ClassificationResult)
def classify_message(commit: CommitMessage):
    """Classify a single commit message"""
    try:
        classification = classify_commit(commit.message)
        suggestions = generate_suggestions(commit.message, classification)
        
        return ClassificationResult(
            message=commit.message,
            type=classification['type'],
            scope=classification['scope'],
            description=classification['description'],
            confidence=classification['confidence'],
            timestamp=datetime.now().isoformat(),
            suggestions=suggestions
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/classify/batch")
def classify_batch(batch: BatchCommitMessages):
    """Classify multiple commit messages"""
    results = []
    
    for msg in batch.messages:
        try:
            classification = classify_commit(msg)
            suggestions = generate_suggestions(msg, classification)
            
            results.append({
                'message': msg,
                'type': classification['type'],
                'scope': classification['scope'],
                'description': classification['description'],
                'confidence': classification['confidence'],
                'timestamp': datetime.now().isoformat(),
                'suggestions': suggestions
            })
        except Exception as e:
            results.append({
                'message': msg,
                'error': str(e)
            })
    
    return {'results': results, 'total': len(results)}

@app.get("/types")
def get_commit_types():
    """Get all commit types and their descriptions"""
    return {
        commit_type: {
            'description': info['description'],
            'keywords': info['keywords'],
            'example': f"{commit_type}: example commit message"
        }
        for commit_type, info in COMMIT_TYPES.items()
    }

@app.get("/stats")
def get_stats():
    """Get API statistics"""
    return {
        'total_commit_types': len(COMMIT_TYPES),
        'supported_types': list(COMMIT_TYPES.keys()),
        'api_version': '1.0.0'
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)