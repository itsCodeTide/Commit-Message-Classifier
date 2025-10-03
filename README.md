# Commit Message Classifier

A full-stack application that classifies git commit messages using conventional commit standards. Built with FastAPI (Python) backend and React frontend.

## Features

- ✅ Classifies commit messages into 11 types (feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert)
- ✅ Extracts scope and description from conventional commits
- ✅ Provides confidence score for classifications
- ✅ Offers suggestions to improve commit messages
- ✅ Beautiful, modern UI with real-time classification
- ✅ Classification history tracking
- ✅ Batch classification support (API)
- ✅ RESTful API with comprehensive endpoints

## Tech Stack

### Backend
- **FastAPI** - Modern, fast Python web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **Regex** - Pattern matching for commit classification

### Frontend
- **React** - UI library
- **Tailwind CSS** - Styling
- **Lucide React** - Icons

## Project Structure

```
commit-message-classifier/
├── backend/
│   ├── main.py              # FastAPI application
│   └── requirements.txt     # Python dependencies
├── frontend/
│   └── src/
│       └── App.jsx          # React application
└── README.md
```

## Installation & Setup

### Backend Setup

1. Navigate to backend directory and create virtual environment:
```bash
cd backend
python -m venv venv
```

2. Activate virtual environment:
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the backend server:
```bash
python main.py
```

Backend will run on `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm start
```

Frontend will run on `http://localhost:3000`

## API Endpoints

### `GET /`
Returns API information and available endpoints.

### `POST /classify`
Classifies a single commit message.

**Request Body:**
```json
{
  "message": "feat: add user authentication"
}
```

**Response:**
```json
{
  "message": "feat: add user authentication",
  "type": "feat",
  "scope": null,
  "description": "add user authentication",
  "confidence": 0.95,
  "timestamp": "2025-10-03T10:30:00",
  "suggestions": []
}
```

### `POST /classify/batch`
Classifies multiple commit messages.

**Request Body:**
```json
{
  "messages": [
    "feat: add login",
    "fix: resolve bug"
  ]
}
```

### `GET /types`
Returns all supported commit types with descriptions and examples.

### `GET /stats`
Returns API statistics.

## Commit Types

| Type | Description |
|------|-------------|
| **feat** | A new feature |
| **fix** | A bug fix |
| **docs** | Documentation changes |
| **style** | Code style changes (formatting, semicolons, etc.) |
| **refactor** | Code refactoring |
| **perf** | Performance improvements |
| **test** | Adding or updating tests |
| **build** | Build system or dependency changes |
| **ci** | CI/CD configuration changes |
| **chore** | Other changes that don't modify src or test files |
| **revert** | Reverts a previous commit |

## How It Works

### Classification Algorithm

1. **Pattern Matching**: First checks if message follows conventional commit format (`type(scope): description`)
2. **Keyword Analysis**: If not conventional format, analyzes keywords to determine type
3. **Confidence Scoring**: Calculates confidence based on pattern match and keyword relevance
4. **Suggestion Generation**: Provides recommendations to improve commit message quality

### Confidence Levels
- **95%**: Perfect conventional format match
- **60-90%**: Keyword-based classification
- **50%**: Default confidence for unclear messages

## Usage Examples

### Good Commit Messages
```
feat(auth): add JWT token validation
fix(api): resolve CORS issue in production
docs: update installation instructions
refactor: optimize database queries
```

### Messages That Need Improvement
```
updated code
fixed stuff
WIP
changes
```

## Testing the API

You can test the API using curl:

```bash
# Single classification
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{"message": "feat: add user authentication"}'

# Batch classification
curl -X POST http://localhost:8000/classify/batch \
  -H "Content-Type: application/json" \
  -d '{"messages": ["feat: new feature", "fix: bug fix"]}'

# Get commit types
curl http://localhost:8000/types
```

## Future Enhancements

- Machine learning model for better classification
- Integration with Git repositories
- VS Code extension
- GitHub Action for commit message validation
- Analytics dashboard for commit patterns
- Custom commit type definitions
- Multi-language support

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes (using proper commit messages!)
4. Push to the branch
5. Create a Pull Request

## License

MIT License - feel free to use this project for your college assignment or any other purpose.

## Author

Created as a college project demonstrating full-stack development with Python and React.

## Screenshots

*Add screenshots of your application here*

## Troubleshooting

### Backend won't start
- Ensure Python 3.8+ is installed
- Check if port 8000 is available
- Verify all dependencies are installed

### Frontend shows connection error
- Ensure backend is running on port 8000
- Check CORS configuration
- Verify API_URL in frontend code

### Classification seems inaccurate
- Algorithm uses keyword matching for non-conventional commits
- Best results with conventional commit format
- Consider contributing to improve classification logic
