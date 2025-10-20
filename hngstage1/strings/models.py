from django.db import models
import hashlib
import json


class AnalyzedString(models.Model):
    """Model to store analyzed strings and their computed properties."""
    
    # Using sha256_hash as the primary key
    id = models.CharField(max_length=64, primary_key=True, editable=False)
    value = models.TextField(unique=True)
    
    # Computed properties
    length = models.IntegerField()
    is_palindrome = models.BooleanField()
    unique_characters = models.IntegerField()
    word_count = models.IntegerField()
    sha256_hash = models.CharField(max_length=64, unique=True)
    character_frequency_map = models.JSONField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        db_table = 'analyzed_strings'
    
    def __str__(self):
        return f"{self.value[:50]}... (ID: {self.id[:8]}...)"
    
    @staticmethod
    def compute_properties(value):
        """Compute all properties for a given string."""
        # SHA-256 hash
        sha256_hash = hashlib.sha256(value.encode('utf-8')).hexdigest()
        
        # Length
        length = len(value)
        
        # Is palindrome (case-insensitive)
        normalized = value.lower()
        is_palindrome = normalized == normalized[::-1]
        
        # Unique characters
        unique_characters = len(set(value))
        
        # Word count
        word_count = len(value.split())
        
        # Character frequency map
        character_frequency_map = {}
        for char in value:
            character_frequency_map[char] = character_frequency_map.get(char, 0) + 1
        
        return {
            'id': sha256_hash,
            'length': length,
            'is_palindrome': is_palindrome,
            'unique_characters': unique_characters,
            'word_count': word_count,
            'sha256_hash': sha256_hash,
            'character_frequency_map': character_frequency_map
        }
    
    def save(self, *args, **kwargs):
        """Override save to compute properties automatically."""
        if not self.id:
            properties = self.compute_properties(self.value)
            self.id = properties['id']
            self.length = properties['length']
            self.is_palindrome = properties['is_palindrome']
            self.unique_characters = properties['unique_characters']
            self.word_count = properties['word_count']
            self.sha256_hash = properties['sha256_hash']
            self.character_frequency_map = properties['character_frequency_map']
        
        super().save(*args, **kwargs)
