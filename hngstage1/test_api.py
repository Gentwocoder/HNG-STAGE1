"""
Test file for the String Analysis API

This file demonstrates how to test all the endpoints using Python requests library.
You can also use tools like Postman or curl to test these endpoints.
"""

import requests
import json

# Base URL - update this if your server is running on a different port
BASE_URL = "http://localhost:8000/strings"


def test_create_string():
    """Test POST /strings - Create/Analyze String"""
    print("\n" + "="*50)
    print("TEST 1: Create/Analyze String")
    print("="*50)
    
    # Test 1: Valid palindrome
    data = {"value": "racecar"}
    response = requests.post(f"{BASE_URL}/", json=data)
    print(f"\nPOST /strings/ with value='racecar'")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 2: Non-palindrome
    data = {"value": "hello world"}
    response = requests.post(f"{BASE_URL}/", json=data)
    print(f"\nPOST /strings/ with value='hello world'")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 3: Duplicate string (should return 409)
    data = {"value": "racecar"}
    response = requests.post(f"{BASE_URL}/", json=data)
    print(f"\nPOST /strings/ with duplicate value='racecar'")
    print(f"Status: {response.status_code} (Expected: 409 Conflict)")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 4: Missing value field (should return 400)
    data = {}
    response = requests.post(f"{BASE_URL}/", json=data)
    print(f"\nPOST /strings/ with missing 'value' field")
    print(f"Status: {response.status_code} (Expected: 400 Bad Request)")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 5: Invalid data type (should return 422)
    data = {"value": 12345}
    response = requests.post(f"{BASE_URL}/", json=data)
    print(f"\nPOST /strings/ with invalid data type (integer)")
    print(f"Status: {response.status_code} (Expected: 422 Unprocessable Entity)")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_get_specific_string():
    """Test GET /strings/{string_value} - Get Specific String"""
    print("\n" + "="*50)
    print("TEST 2: Get Specific String")
    print("="*50)
    
    # Test 1: Valid string
    response = requests.get(f"{BASE_URL}/racecar")
    print(f"\nGET /strings/racecar")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 2: Non-existent string (should return 404)
    response = requests.get(f"{BASE_URL}/nonexistent")
    print(f"\nGET /strings/nonexistent")
    print(f"Status: {response.status_code} (Expected: 404 Not Found)")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_get_all_strings():
    """Test GET /strings - Get All Strings with Filtering"""
    print("\n" + "="*50)
    print("TEST 3: Get All Strings with Filtering")
    print("="*50)
    
    # Create some test data first
    test_strings = [
        "madam",  # palindrome, 1 word
        "A man a plan a canal Panama",  # palindrome, 6 words
        "hello",  # not palindrome, 1 word
        "python programming",  # not palindrome, 2 words
        "noon",  # palindrome, 1 word
    ]
    
    for s in test_strings:
        try:
            requests.post(f"{BASE_URL}/", json={"value": s})
        except:
            pass  # Ignore duplicates
    
    # Test 1: Get all strings
    response = requests.get(f"{BASE_URL}/")
    print(f"\nGET /strings/")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Count: {result['count']}")
    print(f"Filters applied: {result['filters_applied']}")
    
    # Test 2: Filter by palindrome
    response = requests.get(f"{BASE_URL}/?is_palindrome=true")
    print(f"\nGET /strings/?is_palindrome=true")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Count: {result['count']}")
    print(f"Filters applied: {result['filters_applied']}")
    print(f"Results: {[item['value'] for item in result['data']]}")
    
    # Test 3: Filter by word count
    response = requests.get(f"{BASE_URL}/?word_count=1")
    print(f"\nGET /strings/?word_count=1")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Count: {result['count']}")
    print(f"Results: {[item['value'] for item in result['data']]}")
    
    # Test 4: Multiple filters
    response = requests.get(f"{BASE_URL}/?is_palindrome=true&word_count=1")
    print(f"\nGET /strings/?is_palindrome=true&word_count=1")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Count: {result['count']}")
    print(f"Results: {[item['value'] for item in result['data']]}")
    
    # Test 5: Filter by length
    response = requests.get(f"{BASE_URL}/?min_length=5&max_length=10")
    print(f"\nGET /strings/?min_length=5&max_length=10")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Count: {result['count']}")
    print(f"Results: {[item['value'] for item in result['data']]}")
    
    # Test 6: Filter by contains_character
    response = requests.get(f"{BASE_URL}/?contains_character=a")
    print(f"\nGET /strings/?contains_character=a")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Count: {result['count']}")
    print(f"Results: {[item['value'] for item in result['data']]}")


def test_natural_language_filter():
    """Test GET /strings/filter-by-natural-language - Natural Language Filtering"""
    print("\n" + "="*50)
    print("TEST 4: Natural Language Filtering")
    print("="*50)
    
    # Test 1: "all single word palindromic strings"
    query = "all single word palindromic strings"
    response = requests.get(f"{BASE_URL}/filter-by-natural-language?query={query}")
    print(f"\nGET /strings/filter-by-natural-language?query={query}")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Interpreted query: {json.dumps(result['interpreted_query'], indent=2)}")
    print(f"Count: {result['count']}")
    print(f"Results: {[item['value'] for item in result['data']]}")
    
    # Test 2: "strings longer than 10 characters"
    query = "strings longer than 10 characters"
    response = requests.get(f"{BASE_URL}/filter-by-natural-language?query={query}")
    print(f"\nGET /strings/filter-by-natural-language?query={query}")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Interpreted query: {json.dumps(result['interpreted_query'], indent=2)}")
    print(f"Count: {result['count']}")
    print(f"Results: {[item['value'] for item in result['data']]}")
    
    # Test 3: "strings containing the letter z"
    query = "strings containing the letter z"
    response = requests.get(f"{BASE_URL}/filter-by-natural-language?query={query}")
    print(f"\nGET /strings/filter-by-natural-language?query={query}")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Interpreted query: {json.dumps(result['interpreted_query'], indent=2)}")
    print(f"Count: {result['count']}")
    
    # Test 4: "palindromic strings that contain the first vowel"
    query = "palindromic strings that contain the first vowel"
    response = requests.get(f"{BASE_URL}/filter-by-natural-language?query={query}")
    print(f"\nGET /strings/filter-by-natural-language?query={query}")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Interpreted query: {json.dumps(result['interpreted_query'], indent=2)}")
    print(f"Count: {result['count']}")
    print(f"Results: {[item['value'] for item in result['data']]}")


def test_delete_string():
    """Test DELETE /strings/{string_value} - Delete String"""
    print("\n" + "="*50)
    print("TEST 5: Delete String")
    print("="*50)
    
    # Create a test string first
    test_value = "test string to delete"
    requests.post(f"{BASE_URL}/", json={"value": test_value})
    
    # Test 1: Delete existing string
    response = requests.delete(f"{BASE_URL}/{test_value}")
    print(f"\nDELETE /strings/{test_value}")
    print(f"Status: {response.status_code} (Expected: 204 No Content)")
    
    # Test 2: Try to delete non-existent string
    response = requests.delete(f"{BASE_URL}/nonexistent")
    print(f"\nDELETE /strings/nonexistent")
    print(f"Status: {response.status_code} (Expected: 404 Not Found)")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def run_all_tests():
    """Run all tests"""
    print("\n" + "#"*50)
    print("# STRING ANALYSIS API - TEST SUITE")
    print("#"*50)
    
    try:
        test_create_string()
        test_get_specific_string()
        test_get_all_strings()
        test_natural_language_filter()
        test_delete_string()
        
        print("\n" + "#"*50)
        print("# ALL TESTS COMPLETED")
        print("#"*50)
    except requests.exceptions.ConnectionError:
        print("\nERROR: Could not connect to the server.")
        print("Make sure the Django server is running on http://localhost:8000")
        print("Run: python manage.py runserver")
    except Exception as e:
        print(f"\nERROR: {str(e)}")


if __name__ == "__main__":
    run_all_tests()
