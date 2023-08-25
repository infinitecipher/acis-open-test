from django.test import TestCase
from product_generator.serializers import ProductGeneratorSerializer


class TestProductGeneratorSerializer(TestCase):
    """
    Test case for the ProductGeneratorSerializer class.
    """

    def test_valid_serializer(self):
        """
        Test the ProductGeneratorSerializer with valid data.
        """
        data = {
            "product_description": "A totally cool thing",
            "vibe_words": "awesome, extreme",
        }
        serializer = ProductGeneratorSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        validated_data = serializer.validated_data
        self.assertEqual(validated_data["product_description"], "A totally cool thing")
        self.assertEqual(validated_data["vibe_words"], "awesome, extreme")

    def test_missing_fields(self):
        """
        Test the ProductGeneratorSerializer with missing fields.
        """
        data = {}
        serializer = ProductGeneratorSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        errors = serializer.errors
        self.assertIn("product_description", errors)
        self.assertIn("vibe_words", errors)

    def test_empty_fields(self):
        """
        Test the ProductGeneratorSerializer with empty fields.
        """
        data = {
            "product_description": "",
            "vibe_words": "",
        }
        serializer = ProductGeneratorSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        errors = serializer.errors
        self.assertIn("product_description", errors)
        self.assertIn("vibe_words", errors)

    def test_extra_fields(self):
        """
        Test the ProductGeneratorSerializer with extra fields.
        """
        data = {
            "product_description": "Awesome product",
            "vibe_words": "exciting, amazing",
            "extra_field": "This should not be here",
        }
        serializer = ProductGeneratorSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        validated_data = serializer.validated_data
        self.assertEqual(validated_data["product_description"], "Awesome product")
        self.assertEqual(validated_data["vibe_words"], "exciting, amazing")
