from ai_model import SparkApi #因为有__init__.py
from utils import LOG
from enum import Enum, auto
import websocket
from ai_model import Model
from utils import LOG

class SparkModel(Model):
    def __init__(self, api_key: str,api_secret:str,app_id:str, model:str="lite"):
        self.model = model
        if model == "lite":
            self.host = Spark_URL.LITE.value
        else:
            self.host = Spark_URL.LITE.value
        self.app_id = app_id
        self.api_key = api_key
        self.api_secret = api_secret
        
    #这个模式支持的模式列表可以参考
    #https://cloud.baidu.com/doc/WENXINWORKSHOP/s/wm7ltcvgc
    def make_request(self, prompt):
        attempts = 0
        while attempts < 3:
            try:
                SparkApi.answer =""
                print("星火:",end ="")
                question = [{"role": "user", "content": prompt}]
                SparkApi.call(self.app_id,self.api_key,self.api_secret,self.host,self.model,question)
                # print(SparkApi.answer)
                getText(question, "assistant",SparkApi.answer)
                LOG.info(f"SparkApi.answer{SparkApi.answer}")
                return SparkApi.answer, True
            except Exception as e:
                raise Exception(f"发生了未知错误：{e}")
        return "", False

#Spark_url = "wss://spark-api.xf-yun.com/v3.5/chat"   # Max服务地址
#Spark_url = "wss://spark-api.xf-yun.com/v4.0/chat"  # 4.0Ultra服务地址
#Spark_url = "wss://spark-api.xf-yun.com/v3.1/chat"  # Pro服务地址
#Spark_url = "wss://spark-api.xf-yun.com/v1.1/chat"  # Lite服务地址
class Spark_URL(Enum):
    MAX = "wss://spark-api.xf-yun.com/v3.5/chat"
    ULTRA = "wss://spark-api.xf-yun.com/v4.0/chat"
    PRO = "wss://spark-api.xf-yun.com/v3.1/chat"
    LITE = "wss://spark-api.xf-yun.com/v1.1/chat"

def getText(text,role,content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text

def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length

def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text