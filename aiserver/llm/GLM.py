from openai import OpenAI

class GLM:
    def __init__(self):
        # 直接设定参数
        config = {
            "model_name": "GLM-4-Flash-250414",
            "api_key": "06823e29f5c349928ce9acbd77e10fc3.UGAOIG4Mk4S8Kgcb",
            "url": "https://open.bigmodel.cn/api/paas/v4"
        }
        # 使用设定的参数进行初始化
        self.model_name = config.get("model_name")
        self.api_key = config.get("api_key")
        self.url = config.get("url")
        # 创建OpenAI客户端
        self.client = OpenAI(api_key=self.api_key, base_url=self.url)

    # 生成回复方法
    # 传入参数：用户输入对话
    def generate_response(self, user_input):
        # 创建对话
        dialogue = [
            {"role": "system", "content": "调皮的回答"},
            {"role": "user", "content": user_input},
        ]
        # OpenAI客户端生成回复
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=dialogue,
        )
        return response.choices[0].message.content