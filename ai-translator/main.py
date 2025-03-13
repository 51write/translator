import sys
import os
#因为utils、model等包下面都有__init__.py间，且都加载了模块，所以这里能引用到
from utils import ArgumentParser, ConfigLoader, LOG
from ai_model import SparkModel
from translator import PDFTranslator

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()
    config_loader = ConfigLoader(args.config)
    #config_loader = ConfigLoader('.\config.yaml')

    config = config_loader.load_config()

    #默认是spark模型
    model_type = args.model_type if args.model_type else 'SparkModel'
    model_name = args.openpai_model if args.openpai_model else config['SparkModel']['model']
    api_key = args.openapi_api_key if args.openapi_api_key else config['SparkModel']['api_key']
    secret_key = args.openapi_secret_key if args.openapi_secret_key else config['SparkModel']['secret_key']
    app_id = args.openapi_app_id if args.openapi_app_id else config['SparkModel']['appid']
    #secret_key = args.qianfan_secret_key if args.qianfan_secret_key else config['QianFanModel']['secret_key']
    
    model = None
    if model_type and model_type=='SparkModel':
        model = SparkModel(model=model_name, api_key=api_key,api_secret=secret_key,app_id =app_id)


    if(model == None):
        LOG.error(f"初始化模型失败.modelname={model_name}")
    else:
        LOG.info(f"初始化模型成功.modelname={model_name}")
        pdf_file_path = args.book if args.book else config['common']['file']
        file_format = args.file_format if args.file_format else config['common']['file_format']
        # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
        translator = PDFTranslator(model)
        translator.translate_pdf(pdf_file_path, file_format)