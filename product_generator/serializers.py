from rest_framework import serializers


class ProductGeneratorSerializer(serializers.Serializer):
    """
    Serializer for validating and deserializing product generation input.

    This serializer is used to validate and deserialize input data for generating product names,
    ad transcripts, and safety warnings. It defines the structure and validation rules for the input.

    Attributes:
        product_description (CharField): The description of the product.
        vibe_words (CharField): Seed words for generating product content.

    Example:
        payload = {
            "product_description": "A revolutionary gadget for tech enthusiasts",
            "vibe_words": "innovative, futuristic, game-changing"
        }
        serializer = ProductGeneratorSerializer(data=payload)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            # Process the validated data
        else:
            errors = serializer.errors
            # Handle validation errors
    """

    product_description = serializers.CharField()
    vibe_words = serializers.CharField()
