from django.conf import settings

import openai


class OpenAIChat:
    """
    A utility class for interacting with the OpenAI API to generate chat-based responses.

    This class provides methods to generate responses using the OpenAI API for chat-based models.

    Attributes:
        None

    Methods:
        __init__(api_key=None): Constructor for initializing the OpenAIChat instance.
        generate_response(messages, model="gpt-3.5-turbo", temperature=0.8, max_tokens=256):
            Generates a response using the OpenAI API.

    Example:
        chat_instance = OpenAIChat(api_key="your_api_key")
        messages = [{"role": "system", "content": "You are a chatbot."}, {"role": "user", "content": "Hello, how are you?"}]
        response = chat_instance.generate_response(messages)
        print(response)  # Output: "I'm good, thank you! How can I assist you today?"
    """

    def __init__(self, api_key=None):
        """
        Constructor for initializing the OpenAIChat instance.

        :param api_key: Optional API key for OpenAI. If not provided, uses the key from Django settings.
        """
        if api_key is None:
            api_key = settings.OPEN_API_KEY
        openai.api_key = api_key

    def generate_response(
        self, messages, model="gpt-3.5-turbo", temperature=0.8, max_tokens=256
    ):
        """
        Generates a response using the OpenAI API.

        :param messages: List of messages for generating the response.
        :param model: The model to use for generating the response.
        :param temperature: Controls the randomness of the response. Higher values make it more random.
        :param max_tokens: Maximum number of tokens in the generated response.
        :return: Generated response text.
        """
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return response.choices[0].message["content"]
