from unittest.mock import patch, Mock
from django.test import TestCase
from product_generator.utils import OpenAIChat


class TestOpenAIChat(TestCase):
    """
    Test case for the OpenAIChat utility class.
    """

    def setUp(self):
        """
        Set up the test environment by creating an instance of OpenAIChat.
        """
        self.openai_chat = OpenAIChat(api_key="your_mock_api_key")

    def test_generate_response(self):
        """
        Test the generate_response method of the OpenAIChat class.
        """
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        expected_response = "Hello, how can I assist you?"

        mock_choice = Mock()
        mock_choice.message = {"content": expected_response}
        mock_response = Mock()
        mock_response.choices = [mock_choice]

        with patch("openai.ChatCompletion.create", return_value=mock_response):
            response = self.openai_chat.generate_response(messages)

            self.assertEqual(response, expected_response)
