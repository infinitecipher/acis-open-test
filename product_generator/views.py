from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from product_generator.serializers import ProductGeneratorSerializer
from product_generator.utils import OpenAIChat


class GenerateProductView(APIView):
    """
    API view for generating product names, ad transcripts, and safety warnings based on given input.

    This view processes incoming POST requests containing product description and vibe words,
    then generates product names, ad transcripts, and safety warnings using an OpenAI model.

    Attributes:
        None

    Methods:
        post(request, format=None): Handles POST requests for generating product content.
        generate_product_names(openai_instance, product_description, vibe_words):
            Generates product names using OpenAI and provided inputs.
        generate_ad_transcripts(openai_instance, product_names_list):
            Generates ad transcripts for different channels based on product names.
        generate_safety_warning(openai_instance, product_name): Generates a safety warning for a product.
        generate_response(openai_instance, messages): Generates a response using OpenAI and provided messages.

    Example:
        Payload:
        {
            "product_description": "A totally cool thing that makes you 100% more awesome",
            "vibe_words": "awesome, extreme, terrifying"
        }

       Response:
        {
            "product_names": ["AwesomeXtreme Terrorizer","AwesomeXtreme","Extreme Awesome Enhancer"],
            "tv_ad_young_adults": "TV ad response",
            "facebook_ad_parents": "FB ad response",
            "radio_ad_parents": "Radio ad response",
            "safety_warning": "Safety warning response"
        }
    """

    def post(self, request, format=None):
        """
        Generate product names and ad transcripts based on the given input.

        :param request: The HTTP request containing the product description and vibe words.
        :param format: The format of the response data (optional).
        :return: Response containing generated product names and ad transcripts.
        """
        serializer = ProductGeneratorSerializer(data=request.data)
        if serializer.is_valid():
            product_description = serializer.validated_data["product_description"]
            vibe_words = serializer.validated_data["vibe_words"]

            openai_instance = OpenAIChat()

            product_names_list = self.generate_product_names(
                openai_instance, product_description, vibe_words
            )

            ad_transcripts = self.generate_ad_transcripts(
                openai_instance, product_names_list
            )

            safety_warning = self.generate_safety_warning(
                openai_instance, product_names_list[0]
            )

            response_data = {
                "product_names": product_names_list,
                **ad_transcripts,
                "safety_warning": safety_warning,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def generate_product_names(self, openai_instance, product_description, vibe_words):
        """
        Generate product names using the provided OpenAI instance, product description, and vibe words.

        :param openai_instance: An instance of the OpenAIChat class.
        :param product_description: Description of the product.
        :param vibe_words: Seed words for generating product names.
        :return: List of generated product names.
        """
        messages = [
            {
                "role": "system",
                "content": "You will be provided with a product description and seed words, and your task is to generate top 3 product names.",
            },
            {
                "role": "user",
                "content": f"Product description: {product_description}\nSeed words: {vibe_words}.",
            },
        ]
        response = self.generate_response(openai_instance, messages)

        result_list = response.split("\n")

        return result_list

    def generate_ad_transcripts(self, openai_instance, product_names_list):
        """
        Generate ad transcripts for different channels based on product names.

        :param openai_instance: An instance of the OpenAIChat class.
        :param product_names_list: List of generated product names.
        :return: Dictionary of ad transcripts for different channels.
        """
        ad_targets = [
            ("tv_ad_young_adults", "TV", "young adults", 0),
            ("facebook_ad_parents", "Facebook", "parents", 1),
            ("radio_ad_parents", "Radio", "parents", 2),
        ]
        ad_transcripts = {}

        for ad_type, channel, audience, product_index in ad_targets:
            messages = [
                {
                    "role": "system",
                    "content": f"You are a marketing team preparing a {channel} ad for a new product. Target audience: {audience}.",
                },
                {
                    "role": "user",
                    "content": f"Generate a {channel} ad transcript for the product: {product_names_list[product_index]}.",
                },
            ]
            ad_transcripts[ad_type] = self.generate_response(openai_instance, messages)

        return ad_transcripts

    def generate_safety_warning(self, openai_instance, product_name):
        """
        Generate a safety warning for the provided product name.

        :param openai_instance: An instance of the OpenAIChat class.
        :param product_name: Name of the product.
        :return: Generated safety warning.
        """
        messages = [
            {"role": "system", "content": "Write a safety warning for this product"},
            {"role": "user", "content": f"Product: {product_name}."},
        ]
        return self.generate_response(openai_instance, messages)

    def generate_response(self, openai_instance, messages):
        """
        Generate a response using the provided OpenAI instance and messages.

        :param openai_instance: An instance of the OpenAIChat class.
        :param messages: List of messages for generating the response.
        :return: Generated response.
        """
        response = openai_instance.generate_response(messages)
        return response.strip()
