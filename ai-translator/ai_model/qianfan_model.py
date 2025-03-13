import requests
import simplejson
import time
import os
from qianfan import Qianfan,errors
from ai_model import Model
from utils import LOG

class QianFanModel(Model):
    def __init__(self, model: str, api_key: str):
        self.model = model
        self.client = Qianfan(api_key=api_key,app_id='b7c9a832-61ed-480d-818e-11464efbedd8')

    #这个模式支持的模式列表可以参考
    #https://cloud.baidu.com/doc/WENXINWORKSHOP/s/wm7ltcvgc
    def make_request(self, prompt):
        attempts = 0
        while attempts < 3:
            try:
                if self.model == "ERNIE-4.0-Turbo-8K-Latest":
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {"role": "user", "content": prompt}
                        ]
                    )
                    translation = response.choices[0].message.content.strip()
                else:
                    response = self.client.completions.create(
                        model=self.model,
                        prompt=prompt,
                        max_tokens=150,
                        temperature=0
                    )
                    translation = response.choices[0].text.strip()

                return translation, True
            except errors.RequestTimeoutError as e:
                attempts += 1
                if attempts < 3:
                    LOG.warning("Rate limit reached. Waiting for 60 seconds before retrying.")
                    time.sleep(60)
                else:
                    raise Exception("Rate limit reached. Maximum attempts exceeded.")
            except errors.AuthError as e:
                print("验证失败，确认key和secret是否正确")
                print(e.__cause__) 
            except errors.APIError as e:
                print("Another non-200-range status code was received")
                print(e.status_code)
                print(e.response)
            except Exception as e:
                raise Exception(f"发生了未知错误：{e}")
        return "", False