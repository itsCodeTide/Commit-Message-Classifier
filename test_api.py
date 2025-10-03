"""
Test script for Commit Message Classifier API
Run this after starting the backend server
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_root():
    """Test root endpoint"""
    print("\n=== Testing Root Endpoint ===")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_single_classification():
    """Test single message classification"""
    print("\n=== Testing Single Classification ===")
    
    test_messages = [
        "feat: add user authentication",
        "fix(api): resolve CORS issue",
        "docs: update README with installation steps",
        "added new feature",
        "fixed the bug in payment module",
        "refactor: optimize database queries"
    ]
    
    for msg in test_messages:
        print(f"\nMessage: {msg}")
        response = requests.post(
            f"{BASE_URL}/classify",
            json={"message": msg}
        )
        if response.status_code == 200:
            result = response.json()
            print(f"  Type: {result['type']}")
            print(f"  Confidence: {result['confidence']:.2%}")
            print(f"  Suggestions: {len(result['suggestions'])} found")
        else:
            print(f"  Error: {response.status_code}")

def test_batch_classification():
    """Test batch classification"""
    print("\n=== Testing Batch Classification ===")
    
    messages = [
        "feat: add login feature",
        "fix: resolve security vulnerability",
        "docs: add API documentation",
        "test: add unit tests for auth module"
    ]
    
    response = requests.post(
        f"{BASE_URL}/classify/batch",
        json={"messages": messages}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"Total processed: {result['total']}")
        for i, res in enumerate(result['results'], 1):
            print(f"\n{i}. {res['message']}")
            print(f"   Type: {res['type']} | Confidence: {res['confidence']:.2%}")
    else:
        print(f"Error: {response.status_code}")

def test_get_types():
    """Test get commit types endpoint"""
    print("\n=== Testing Get Types Endpoint ===")
    response = requests.get(f"{BASE_URL}/types")
    if response.status_code == 200:
        types = response.json()
        print(f"Total commit types: {len(types)}")
        for commit_type, info in types.items():
            print(f"\n{commit_type}: {info['description']}")
            print(f"  Keywords: {', '.join(info['keywords'][:3])}...")
    else:
        print(f"Error: {response.status_code}")

def test_stats():
    """Test stats endpoint"""
    print("\n=== Testing Stats Endpoint ===")
    response = requests.get(f"{BASE_URL}/stats")
    if response.status_code == 200:
        stats = response.json()
        print(f"Stats: {json.dumps(stats, indent=2)}")
    else:
        print(f"Error: {response.status_code}")

def run_all_tests():
    """Run all tests"""
    try:
        print("Starting API Tests...")
        print("=" * 50)
        
        test_root()
        test_single_classification()
        test_batch_classification()
        test_get_types()
        test_stats()
        
        print("\n" + "=" * 50)
        print("All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("\nError: Cannot connect to backend server.")
        print("Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    run_all_tests()