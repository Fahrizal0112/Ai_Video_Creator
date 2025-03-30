from openai import OpenAI

class ContentGenerator:
    def __init__(self):
        self.client = OpenAI(api_key="your-openai-api-key")
    
    def generate_content(self):
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Buat script video TikTok yang viral"},
                {"role": "user", "content": "Buatkan script video pendek"}
            ]
        )
        
        return {
            "script": response.choices[0].message.content,
            "duration": 60,
            "style": "entertaining"
        }