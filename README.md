# String Analysis RESTful API

A Django REST Framework API service that analyzes strings and stores their computed properties.

## Features

For each analyzed string, the API computes and stores:
- **length**: Number of characters in the string
- **is_palindrome**: Boolean indicating if the string reads the same forwards and backwards (case-insensitive)
- **unique_characters**: Count of distinct characters in the string
- **word_count**: Number of words separated by whitespace
- **sha256_hash**: SHA-256 hash of the string for unique identification
- **character_frequency_map**: Dictionary mapping each character to its occurrence count

## Installation

1. **Clone the repository** (if applicable)

2. **Install dependencies**:
   ```bash
   pip install django djangorestframework
   ```

3. **Run migrations**:
   ```bash
   cd hngstage1
   python manage.py migrate
   ```

4. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. Create/Analyze String

**Endpoint**: `POST /strings/`

**Request Body**:
```json
{
  "value": "string to analyze"
}
```

**Success Response (201 Created)**:
```json
{
  "id": "sha256_hash_value",
  "value": "string to analyze",
  "properties": {
    "length": 16,
    "is_palindrome": false,
    "unique_characters": 12,
    "word_count": 3,
    "sha256_hash": "abc123...",
    "character_frequency_map": {
      "s": 2,
      "t": 3,
      "r": 2
    }
  },
  "created_at": "2025-08-27T10:00:00Z"
}
```

**Error Responses**:
- `409 Conflict`: String already exists in the system
- `400 Bad Request`: Invalid request body or missing "value" field
- `422 Unprocessable Entity`: Invalid data type for "value" (must be string)

**Example**:
```bash
curl -X POST http://localhost:8000/strings/ \
  -H "Content-Type: application/json" \
  -d '{"value": "racecar"}'
```

---

### 2. Get Specific String

**Endpoint**: `GET /strings/{string_value}`

**Success Response (200 OK)**:
```json
{
  "id": "sha256_hash_value",
  "value": "requested string",
  "properties": {
    "length": 16,
    "is_palindrome": false,
    "unique_characters": 12,
    "word_count": 3,
    "sha256_hash": "abc123...",
    "character_frequency_map": {}
  },
  "created_at": "2025-08-27T10:00:00Z"
}
```

**Error Responses**:
- `404 Not Found`: String does not exist in the system

**Example**:
```bash
curl http://localhost:8000/strings/racecar
```

---

### 3. Get All Strings with Filtering

**Endpoint**: `GET /strings/`

**Query Parameters**:
- `is_palindrome`: boolean (true/false)
- `min_length`: integer (minimum string length)
- `max_length`: integer (maximum string length)
- `word_count`: integer (exact word count)
- `contains_character`: string (single character to search for)

**Success Response (200 OK)**:
```json
{
  "data": [
    {
      "id": "hash1",
      "value": "string1",
      "properties": {},
      "created_at": "2025-08-27T10:00:00Z"
    }
  ],
  "count": 15,
  "filters_applied": {
    "is_palindrome": true,
    "min_length": 5,
    "max_length": 20,
    "word_count": 2,
    "contains_character": "a"
  }
}
```

**Error Response**:
- `400 Bad Request`: Invalid query parameter values or types

**Examples**:
```bash
# Get all palindromes
curl http://localhost:8000/strings/?is_palindrome=true

# Get strings with exactly 2 words
curl http://localhost:8000/strings/?word_count=2

# Get strings between 5 and 20 characters
curl http://localhost:8000/strings/?min_length=5&max_length=20

# Get strings containing 'a'
curl http://localhost:8000/strings/?contains_character=a

# Combine multiple filters
curl http://localhost:8000/strings/?is_palindrome=true&word_count=1
```

---

### 4. Natural Language Filtering

**Endpoint**: `GET /strings/filter-by-natural-language`

**Query Parameters**:
- `query`: Natural language query string

**Success Response (200 OK)**:
```json
{
  "data": [],
  "count": 3,
  "interpreted_query": {
    "original": "all single word palindromic strings",
    "parsed_filters": {
      "word_count": 1,
      "is_palindrome": true
    }
  }
}
```

**Supported Query Patterns**:
- "all single word palindromic strings" → `word_count=1, is_palindrome=true`
- "strings longer than 10 characters" → `min_length=11`
- "strings shorter than 5 characters" → `max_length=4`
- "palindromic strings that contain the first vowel" → `is_palindrome=true, contains_character=a`
- "strings containing the letter z" → `contains_character=z`

**Error Responses**:
- `400 Bad Request`: Unable to parse natural language query
- `422 Unprocessable Entity`: Query parsed but resulted in conflicting filters

**Examples**:
```bash
# Find single word palindromes
curl "http://localhost:8000/strings/filter-by-natural-language?query=all%20single%20word%20palindromic%20strings"

# Find long strings
curl "http://localhost:8000/strings/filter-by-natural-language?query=strings%20longer%20than%2010%20characters"

# Find strings with specific character
curl "http://localhost:8000/strings/filter-by-natural-language?query=strings%20containing%20the%20letter%20z"
```

---

### 5. Delete String

**Endpoint**: `DELETE /strings/{string_value}`

**Success Response**: `204 No Content` (empty response body)

**Error Responses**:
- `404 Not Found`: String does not exist in the system

**Example**:
```bash
curl -X DELETE http://localhost:8000/strings/racecar
```

---

## Testing

A comprehensive test suite is provided in `test_api.py`. To run the tests:

1. **Start the Django server**:
   ```bash
   python manage.py runserver
   ```

2. **In another terminal, install requests** (if not already installed):
   ```bash
   pip install requests
   ```

3. **Run the test suite**:
   ```bash
   python test_api.py
   ```

OR

**Run the test script**
  ```bash
   ./test_api.sh
  ```
The test suite will:
- Create various strings with different properties
- Test all API endpoints
- Verify error handling
- Test filtering and natural language queries

## Project Structure

```
hngstage1/
├── manage.py
├── hngstage1/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── strings/
│   ├── models.py          # AnalyzedString model
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API views
│   ├── urls.py            # URL routing
│   └── migrations/
└── test_api.py            # Test suite
```

## Implementation Details

### String Analysis Algorithm

The string analysis is performed in the `AnalyzedString.compute_properties()` static method:

1. **SHA-256 Hash**: Generated using Python's `hashlib` library
2. **Length**: Simple `len()` function
3. **Palindrome Check**: Case-insensitive comparison with reversed string
4. **Unique Characters**: Count of distinct characters using `set()`
5. **Word Count**: Split by whitespace using `split()`
6. **Character Frequency**: Dictionary comprehension counting each character

### Natural Language Query Parsing

The natural language parser uses regular expressions to identify:
- Palindrome keywords: "palindrome", "palindromic"
- Word count: "single word", "two word", "3 words", etc.
- Length constraints: "longer than X", "shorter than X", "at least X", "at most X"
- Character containment: "containing the letter X", "with the letter X"
- Vowel references: "first vowel" (a), "second vowel" (e), etc.

## Technical Stack

- **Django 4.2.14**: Web framework
- **Django REST Framework**: RESTful API toolkit
- **SQLite**: Database (default Django database)
- **Python 3.x**: Programming language

## Notes

- All strings are stored with unique SHA-256 hashes as identifiers
- Duplicate strings are rejected with a 409 Conflict error
- Palindrome checking is case-insensitive
- The API uses JSON for all request and response bodies
- All timestamps are in UTC (ISO 8601 format)

## License

This project is created for the HNG Stage 1 task.
