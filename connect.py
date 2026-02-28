from openai import OpenAI

class LLM:

    def __init__(self, config):
        self.model_name = config.get("model_name")
        self.api_key = config.get("api_key")
        self.url = config.get("url")
        self.client = OpenAI(api_key=self.api_key, base_url=self.url)

    def generate_response(self, dialogue):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=dialogue,
        )
        return response.choices[0].message.content

def run():
    prompt = "你好"
    config = {
        "model_name": "GLM-4-Flash-250414",
        "api_key": "06823e29f5c349928ce9acbd77e10fc3.UGAOIG4Mk4S8Kgcb",
        "url": "https://open.bigmodel.cn/api/paas/v4"
    }
    llm = LLM(config)

    dialogue = [
        {"role": "system", "content": "严肃的官方的回答"},
        {"role": "user", "content": "你是谁"},
    ]

    resource = llm.generate_response(dialogue)

    print(resource)

if __name__ == "__main__":
    run()