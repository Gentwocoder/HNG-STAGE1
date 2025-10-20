#!/bin/bash
# API Testing Script - String Analysis API
# Make sure the Django server is running: python manage.py runserver

BASE_URL="http://localhost:8000/strings"

echo "=========================================="
echo "String Analysis API - Test Commands"
echo "=========================================="

echo -e "\n1. CREATE/ANALYZE STRINGS"
echo "Creating 'racecar' (palindrome)..."
curl -X POST $BASE_URL/ \
  -H "Content-Type: application/json" \
  -d '{"value": "racecar"}' \
  -w "\nStatus: %{http_code}\n\n"

echo "Creating 'hello world' (not palindrome)..."
curl -X POST $BASE_URL/ \
  -H "Content-Type: application/json" \
  -d '{"value": "hello world"}' \
  -w "\nStatus: %{http_code}\n\n"

echo "Creating 'madam' (palindrome)..."
curl -X POST $BASE_URL/ \
  -H "Content-Type: application/json" \
  -d '{"value": "madam"}' \
  -w "\nStatus: %{http_code}\n\n"

echo "Creating 'noon' (palindrome)..."
curl -X POST $BASE_URL/ \
  -H "Content-Type: application/json" \
  -d '{"value": "noon"}' \
  -w "\nStatus: %{http_code}\n\n"

echo "Creating 'python programming' (not palindrome, 2 words)..."
curl -X POST $BASE_URL/ \
  -H "Content-Type: application/json" \
  -d '{"value": "python programming"}' \
  -w "\nStatus: %{http_code}\n\n"

echo -e "\n2. GET SPECIFIC STRING"
echo "Getting 'racecar'..."
curl -X GET $BASE_URL/racecar \
  -w "\nStatus: %{http_code}\n\n"

echo -e "\n3. GET ALL STRINGS (No Filter)"
echo "Getting all strings..."
curl -X GET $BASE_URL/ \
  -w "\nStatus: %{http_code}\n\n"

echo -e "\n4. FILTER BY PALINDROME"
echo "Getting all palindromes..."
curl -X GET "$BASE_URL/?is_palindrome=true" \
  -w "\nStatus: %{http_code}\n\n"

echo -e "\n5. FILTER BY WORD COUNT"
echo "Getting single word strings..."
curl -X GET "$BASE_URL/?word_count=1" \
  -w "\nStatus: %{http_code}\n\n"

echo -e "\n6. MULTIPLE FILTERS"
echo "Getting single word palindromes..."
curl -X GET "$BASE_URL/?is_palindrome=true&word_count=1" \
  -w "\nStatus: %{http_code}\n\n"

echo -e "\n7. FILTER BY LENGTH"
echo "Getting strings between 5 and 10 characters..."
curl -X GET "$BASE_URL/?min_length=5&max_length=10" \
  -w "\nStatus: %{http_code}\n\n"

echo -e "\n8. NATURAL LANGUAGE QUERY"
echo "Query: 'all single word palindromic strings'"
curl -X GET "$BASE_URL/filter-by-natural-language?query=all%20single%20word%20palindromic%20strings" \
  -w "\nStatus: %{http_code}\n\n"

echo -e "\n9. ERROR CASES"
echo "Duplicate string (409 Conflict)..."
curl -X POST $BASE_URL/ \
  -H "Content-Type: application/json" \
  -d '{"value": "racecar"}' \
  -w "\nStatus: %{http_code}\n\n"

echo "Missing value field (400 Bad Request)..."
curl -X POST $BASE_URL/ \
  -H "Content-Type: application/json" \
  -d '{}' \
  -w "\nStatus: %{http_code}\n\n"

echo "Invalid data type (422 Unprocessable Entity)..."
curl -X POST $BASE_URL/ \
  -H "Content-Type: application/json" \
  -d '{"value": 12345}' \
  -w "\nStatus: %{http_code}\n\n"

echo "Non-existent string (404 Not Found)..."
curl -X GET $BASE_URL/nonexistent \
  -w "\nStatus: %{http_code}\n\n"

echo -e "\n10. DELETE STRING"
echo "Deleting 'hello world'..."
curl -X DELETE "$BASE_URL/hello world" \
  -w "\nStatus: %{http_code}\n\n"

echo "=========================================="
echo "Tests Completed!"
echo "=========================================="
