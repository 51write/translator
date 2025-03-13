import sys
import os
#因为utils、model等包下面都有__init__.py间，且都加载了模块，所以这里能引用到
from utils import ArgumentParser, ConfigLoader, LOG
from ai_model import SparkModel
from translator import PDFTranslator
from ai_model import Model
import streamlit as st
import base64
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import chardet

pdf_file_path =""
file_format = ""
page=1
model = None

def get_sub_dir(current_dir:str, sub_dir):
    dir = os.path.join(current_dir,sub_dir)
    if not os.path.exists(dir):
        os.mkdir(dir)
    return dir

def getModel()-> Model:
    current_dir = os.getcwd()
    config_path = os.path.join(current_dir,'config.yaml')
 
    config_loader = ConfigLoader(config_path)
    config = config_loader.load_config()

    #默认是spark模型
    LOG.info(f"os.getenv('model_type')={os.getenv('model_type')}")
    model_type = os.getenv('model_type') if os.getenv('model_type') else 'SparkModel'
    model_name = os.getenv('openpai_model') if os.getenv('openpai_model') else config['SparkModel']['model']
    api_key = os.getenv('openapi_api_key') if os.getenv('openapi_api_key') else config['SparkModel']['api_key']
    secret_key = os.getenv('openapi_secret_key') if os.getenv('openapi_secret_key') else config['SparkModel']['secret_key']
    app_id = os.getenv('openapi_app_id') if os.getenv('openapi_app_id') else config['SparkModel']['app_id']
    
    model = None
    if model_type and model_type=='SparkModel':
        model = SparkModel(model=model_name, api_key=api_key,api_secret=secret_key,app_id =app_id)

    if(model == None):
        LOG.error(f"初始化模型失败.modelname={model_name}")
    else:
        LOG.info(f"初始化模型成功.modelname={model_name}")
    return model

#上传文件，保存到test目录下面，这样是为了方便后续的重试场景
st.header('中英文翻译')
uploaded_file = st.file_uploader("请选择一个pdf，注意不能是扫描版的",type=["pdf"])
if uploaded_file is not None:
    st.write("文件名:",uploaded_file.name)

    current_dir = get_sub_dir(os.getcwd(),"tests")
    file_path = os.path.join(current_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    st.success(f"文件 '{uploaded_file.name}' 已成功保存到 {current_dir} 目录下！")
    pdf_file_path = file_path

###显示out的类型和目标语言
st.header('输出文件类型')
file_format = st.selectbox('文档格式',['markdown','pdf'],disabled=False)

st.header('最大页数')
page = st.selectbox('page',['50','100'],disabled=False)   

if st.button("翻译"):
    try:
        output_dir = get_sub_dir(os.getcwd(),"out")
        output_file_path = os.path.join(output_dir, '翻译结果.' + file_format)
        print(f"output_file_path={output_file_path}")
        model = getModel()
    
        translator = PDFTranslator(model)
        translator.translate_pdf(pdf_file_path=pdf_file_path, file_format=file_format,output_file_path=output_file_path)

        print(f"文件保存的地址是{file_path}")
        # 读取文件内容
        with open(output_file_path ,"rb") as file:
            raw_data = file.read()

        try:
            content = raw_data.decode('utf-8')
        except UnicodeDecodeError:
            LOG.info(f"解码失败，尝试使用gbk")
            content = raw_data.decode('gbk')  # 或其他可能的编码

        st.download_button(
            label="下载翻译结果",
            data=content,
            file_name='翻译结果.' + file_format,
            mime="text/markdown",
            
        )
    except Exception as e:
        LOG.error(e.__cause__) 
        raise Exception(f"发生了未知错误：{e}")

