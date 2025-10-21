from rest_framework import serializers
from .models import AnalyzedString


class AnalyzedStringSerializer(serializers.ModelSerializer):
    """Serializer for AnalyzedString model."""
    
    properties = serializers.SerializerMethodField()
    
    class Meta:
        model = AnalyzedString
        fields = ['id', 'value', 'properties', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_properties(self, obj):
        """Return computed properties as a nested object."""
        return {
            'length': obj.length,
            'is_palindrome': obj.is_palindrome,
            'unique_characters': obj.unique_characters,
            'word_count': obj.word_count,
            'sha256_hash': obj.sha256_hash,
            'character_frequency_map': obj.character_frequency_map
        }
    
    def validate_value(self, value):
        """Validate that value is a string."""
        if not isinstance(value, str):
            raise serializers.ValidationError("Value must be a string.")
        return value


class CreateStringSerializer(serializers.Serializer):
    """Serializer for creating a new analyzed string."""
    
    value = serializers.CharField(allow_blank=True)
    
    def validate(self, data):
        """Validate the entire input data before field-level validation."""
        # Check the raw initial data for type validation
        if 'value' in self.initial_data:
            raw_value = self.initial_data['value']
            if not isinstance(raw_value, str):
                raise serializers.ValidationError({
                    'value': 'Value must be a string.'
                })
        return data
    
    def validate_value(self, value):
        """Validate that value is a string."""
        if not isinstance(value, str):
            raise serializers.ValidationError("Value must be a string.")
        return value
    
    def create(self, validated_data):
        """Create a new AnalyzedString instance."""
        return AnalyzedString.objects.create(**validated_data)
