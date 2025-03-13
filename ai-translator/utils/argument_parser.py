import argparse

class ArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Translate English PDF book to Chinese.')
        self.parser.add_argument('--config', type=str, default='config.yaml', help='Configuration file with model and API settings.')
        self.parser.add_argument('--model_type', type=str, required=True, choices=['QianFanModel','SparkModel'], help='The type of translation model to use. Choose between "QianFanModel" and "other".')        
        self.parser.add_argument('--timeout', type=int, help='Timeout for the API request in seconds.')
        self.parser.add_argument('--openpai_model', type=str, help='The model name of Qianfan Model. Required if model_type is "QianfanModel".')
        self.parser.add_argument('--openapi_api_key', type=str, help='The API key for QianfanModel. Required if model_type is "QianfanModel".')
        self.parser.add_argument('--openapi_secret_key', type=str, help='The Secret key for QianfanModel. Required if model_type is "QianfanModel".')
        self.parser.add_argument('--openapi_app_id', type=str, help='The Secret key for QianfanModel. Required if model_type is "QianfanModel".')
        self.parser.add_argument('--book', type=str, help='PDF file to translate.')
        self.parser.add_argument('--file_format', type=str, help='The file format of translated book. Now supporting PDF and Markdown')

    def parse_arguments(self):
        args = self.parser.parse_args()
        if args.model_type == 'QianfanModel' and not args.openpai_model and not args.openapi_api_key:
            self.parser.error("--openpai_model and --openapi_api_key is required when using OpenAIModel")
        elif args.model_type == 'SparkModel' and not args.openpai_model and not args.openapi_api_key and not ars.openapi_secret_key and not openapi_app_id:
            self.parser.error("--openpai_model and --openapi_api_key and is --openapi_secret_key and --openapi_app_id when using SparkModel")
        return args