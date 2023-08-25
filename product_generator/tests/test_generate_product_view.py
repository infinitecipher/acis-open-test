import unittest

from unittest.mock import patch
from django.urls import reverse_lazy
from rest_framework.test import APITestCase
from rest_framework import status
from product_generator.views import GenerateProductView


class TestGenerateProductViewMethods(unittest.TestCase):
    """
    Unit tests for methods in the GenerateProductView class.
    """

    @patch("product_generator.utils.OpenAIChat")
    def setUp(self, MockOpenAIChat):
        """
        Set up the test environment by creating mock instances and objects.
        """
        self.view_instance = GenerateProductView()
        self.mock_openai_instance = MockOpenAIChat.return_value

    def test_generate_product_names(self):
        """
        Test the generate_product_names method.
        """
        product_description = "A totally cool thing"
        vibe_words = "awesome, extreme"
        raw_response = "AwesomeMix\nAwesomeProduct\nAwesomeTest"
        expected_response = ["AwesomeMix", "AwesomeProduct", "AwesomeTest"]

        self.mock_openai_instance.generate_response.return_value = raw_response

        result = self.view_instance.generate_product_names(
            self.mock_openai_instance, product_description, vibe_words
        )

        self.assertEqual(result, expected_response)

    def test_generate_ad_transcripts(self):
        """
        Test the generate_ad_transcripts method.
        """
        products = ["AwesomeMix", "AwesomeProduct", "AwesomeTest"]
        raw_response = "Transcript for each channel"
        expected_response = {
            "tv_ad_young_adults": raw_response,
            "facebook_ad_parents": raw_response,
            "radio_ad_parents": raw_response,
        }

        self.mock_openai_instance.generate_response.return_value = raw_response

        result = self.view_instance.generate_ad_transcripts(
            self.mock_openai_instance, products
        )

        self.assertEqual(result, expected_response)

    def test_generate_safety_warning(self):
        """
        Test the generate_safety_warning method.
        """
        product = "AwesomeMix"
        expected_response = "Safety warning."

        self.mock_openai_instance.generate_response.return_value = expected_response

        result = self.view_instance.generate_safety_warning(
            self.mock_openai_instance, product
        )

        self.assertEqual(result, expected_response)

    def test_generate_response(self):
        """
        Test the generate_response method.
        """
        messages = [
            {"role": "system", "content": "Test system message."},
            {"role": "user", "content": "Test user message."},
        ]

        expected_response = "Sample OpenAI response."

        self.mock_openai_instance.generate_response.return_value = expected_response

        result = self.view_instance.generate_response(
            self.mock_openai_instance, messages
        )

        self.assertEqual(result, expected_response)


class TestGenerateProductViewIntegration(APITestCase):
    """
    Integration tests for the GenerateProductView API endpoint.
    """

    def test_generate_product_view(self):
        """
        Test the generate_product_view API endpoint.
        """
        url = reverse_lazy("product_generator:generate_product")
        data = {
            "product_description": "A totally cool thing",
            "vibe_words": "awesome, extreme",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("product_names", response.data)
        self.assertIn("tv_ad_young_adults", response.data)
        self.assertIn("facebook_ad_parents", response.data)
        self.assertIn("radio_ad_parents", response.data)
        self.assertIn("safety_warning", response.data)
