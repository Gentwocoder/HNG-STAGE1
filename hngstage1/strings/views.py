from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import IntegrityError
from django.db.models import Q
from .models import AnalyzedString
from .serializers import AnalyzedStringSerializer, CreateStringSerializer
import re


class StringListCreateView(APIView):
    """
    GET /strings - List all strings with optional filtering
    POST /strings - Create/Analyze a new string
    """
    
    def get(self, request):
        """Get all strings with optional filtering."""
        try:
            queryset = AnalyzedString.objects.all()
            filters_applied = {}
            
            # Apply filters based on query parameters
            is_palindrome = request.query_params.get('is_palindrome')
            min_length = request.query_params.get('min_length')
            max_length = request.query_params.get('max_length')
            word_count = request.query_params.get('word_count')
            contains_character = request.query_params.get('contains_character')
            
            if is_palindrome is not None:
                # Convert to boolean
                if is_palindrome.lower() == 'true':
                    queryset = queryset.filter(is_palindrome=True)
                    filters_applied['is_palindrome'] = True
                elif is_palindrome.lower() == 'false':
                    queryset = queryset.filter(is_palindrome=False)
                    filters_applied['is_palindrome'] = False
                else:
                    return Response(
                        {"error": "Invalid value for is_palindrome. Use 'true' or 'false'."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            if min_length is not None:
                try:
                    min_length = int(min_length)
                    queryset = queryset.filter(length__gte=min_length)
                    filters_applied['min_length'] = min_length
                except ValueError:
                    return Response(
                        {"error": "Invalid value for min_length. Must be an integer."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            if max_length is not None:
                try:
                    max_length = int(max_length)
                    queryset = queryset.filter(length__lte=max_length)
                    filters_applied['max_length'] = max_length
                except ValueError:
                    return Response(
                        {"error": "Invalid value for max_length. Must be an integer."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            if word_count is not None:
                try:
                    word_count = int(word_count)
                    queryset = queryset.filter(word_count=word_count)
                    filters_applied['word_count'] = word_count
                except ValueError:
                    return Response(
                        {"error": "Invalid value for word_count. Must be an integer."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            if contains_character is not None:
                if len(contains_character) != 1:
                    return Response(
                        {"error": "contains_character must be a single character."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                queryset = queryset.filter(value__icontains=contains_character)
                filters_applied['contains_character'] = contains_character
            
            serializer = AnalyzedStringSerializer(queryset, many=True)
            
            return Response({
                'data': serializer.data,
                'count': queryset.count(),
                'filters_applied': filters_applied
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def post(self, request):
        """Create and analyze a new string."""
        # Validate request body
        if 'value' not in request.data:
            return Response(
                {"error": "Missing 'value' field in request body."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = CreateStringSerializer(data=request.data)
        
        if not serializer.is_valid():
            # Check if it's a type error
            if 'value' in serializer.errors:
                return Response(
                    {"error": "Invalid data type for 'value'. Must be a string."},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Create the analyzed string
            analyzed_string = serializer.save()
            response_serializer = AnalyzedStringSerializer(analyzed_string)
            
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )
        
        except IntegrityError:
            return Response(
                {"error": "String already exists in the system."},
                status=status.HTTP_409_CONFLICT
            )
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )


class StringDetailView(APIView):
    """
    GET /strings/{string_value} - Get a specific string
    DELETE /strings/{string_value} - Delete a specific string
    """
    
    def get(self, request, string_value):
        """Get a specific string by its value."""
        try:
            analyzed_string = AnalyzedString.objects.get(value=string_value)
            serializer = AnalyzedStringSerializer(analyzed_string)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AnalyzedString.DoesNotExist:
            return Response(
                {"error": "String does not exist in the system."},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def delete(self, request, string_value):
        """Delete a specific string by its value."""
        try:
            analyzed_string = AnalyzedString.objects.get(value=string_value)
            analyzed_string.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AnalyzedString.DoesNotExist:
            return Response(
                {"error": "String does not exist in the system."},
                status=status.HTTP_404_NOT_FOUND
            )


class NaturalLanguageFilterView(APIView):
    """
    GET /strings/filter-by-natural-language - Filter strings using natural language query
    """
    
    def parse_natural_language_query(self, query):
        """Parse natural language query into filter parameters."""
        query_lower = query.lower().strip()
        filters = {}
        
        # Check for palindrome
        if 'palindrome' in query_lower or 'palindromic' in query_lower:
            filters['is_palindrome'] = True
        
        # Check for word count
        if 'single word' in query_lower or 'one word' in query_lower:
            filters['word_count'] = 1
        elif 'two word' in query_lower or '2 word' in query_lower:
            filters['word_count'] = 2
        elif 'three word' in query_lower or '3 word' in query_lower:
            filters['word_count'] = 3
        else:
            # Try to extract number followed by "word" or "words"
            word_count_match = re.search(r'(\d+)\s*words?', query_lower)
            if word_count_match:
                filters['word_count'] = int(word_count_match.group(1))
        
        # Check for length constraints
        # "longer than X characters" or "more than X characters"
        longer_match = re.search(r'(?:longer|more)\s+than\s+(\d+)\s*(?:character|char)', query_lower)
        if longer_match:
            filters['min_length'] = int(longer_match.group(1)) + 1
        
        # "shorter than X characters" or "less than X characters"
        shorter_match = re.search(r'(?:shorter|less)\s+than\s+(\d+)\s*(?:character|char)', query_lower)
        if shorter_match:
            filters['max_length'] = int(shorter_match.group(1)) - 1
        
        # "at least X characters"
        at_least_match = re.search(r'at\s+least\s+(\d+)\s*(?:character|char)', query_lower)
        if at_least_match:
            filters['min_length'] = int(at_least_match.group(1))
        
        # "at most X characters"
        at_most_match = re.search(r'at\s+most\s+(\d+)\s*(?:character|char)', query_lower)
        if at_most_match:
            filters['max_length'] = int(at_most_match.group(1))
        
        # Check for specific character containment
        # "containing the letter X" or "with the letter X"
        letter_match = re.search(r'(?:containing|with|contain)\s+(?:the\s+)?(?:letter|character)\s+([a-z])', query_lower)
        if letter_match:
            filters['contains_character'] = letter_match.group(1)
        
        # Check for vowel references
        if 'first vowel' in query_lower:
            filters['contains_character'] = 'a'
        elif 'second vowel' in query_lower:
            filters['contains_character'] = 'e'
        elif 'third vowel' in query_lower:
            filters['contains_character'] = 'i'
        elif 'fourth vowel' in query_lower:
            filters['contains_character'] = 'o'
        elif 'fifth vowel' in query_lower:
            filters['contains_character'] = 'u'
        
        return filters
    
    def get(self, request):
        """Filter strings using natural language query."""
        query = request.query_params.get('query', '')
        
        if not query:
            return Response(
                {"error": "Missing 'query' parameter."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Parse the natural language query
            parsed_filters = self.parse_natural_language_query(query)
            
            if not parsed_filters:
                return Response(
                    {"error": "Unable to parse natural language query."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Apply filters to queryset
            queryset = AnalyzedString.objects.all()
            
            if 'is_palindrome' in parsed_filters:
                queryset = queryset.filter(is_palindrome=parsed_filters['is_palindrome'])
            
            if 'min_length' in parsed_filters:
                queryset = queryset.filter(length__gte=parsed_filters['min_length'])
            
            if 'max_length' in parsed_filters:
                queryset = queryset.filter(length__lte=parsed_filters['max_length'])
            
            if 'word_count' in parsed_filters:
                queryset = queryset.filter(word_count=parsed_filters['word_count'])
            
            if 'contains_character' in parsed_filters:
                queryset = queryset.filter(value__icontains=parsed_filters['contains_character'])
            
            serializer = AnalyzedStringSerializer(queryset, many=True)
            
            return Response({
                'data': serializer.data,
                'count': queryset.count(),
                'interpreted_query': {
                    'original': query,
                    'parsed_filters': parsed_filters
                }
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

