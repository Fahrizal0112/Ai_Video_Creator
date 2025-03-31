# content_generator.py
import google.generativeai as genai

class ContentGenerator:
    def __init__(self):
        genai.configure(api_key="AIzaSyAB4o8VpccbEeM_jlCOIezJGYRDoA488Ig")
        self.model = genai.GenerativeModel('gemini-2.5-pro-exp-03-25')
    
    def generate_content(self):
        prompt = """
        Buatkan script komedi pendek dengan karakter yang agak nyeleneh.
        Format output HARUS PERSIS seperti ini:
        
        KARAKTER: [Deskripsi karakter]
        VOICE_PRESET: male_funny
        MOOD: [Mood karakter]
        SETTING: [Deskripsi setting]
        
        DIALOG:
        - [EXCITED] "Halo gaes!" [ekspresi: senang]
        - [SURPRISED] "Anjir, gak nyangka!" [ekspresi: kaget]
        - [ANGRY] "Dasar jembut!" [ekspresi: kesal]
        
        SOUND_EFFECT: laugh, boom, ding
        
        HASHTAG: #viral #comedy #lucu #trending #fyp
        
        Markup emosi yang tersedia: [EXCITED], [SURPRISED], [ANGRY], [HAPPY], [SAD]
        """
        
        response = self.model.generate_content(prompt)
        return {
            "script": response.text,
            "duration": 30,
            "style": "comedy"
        }
    
    def parse_response(self, text):
        expressions = []
        movements = []
        
        lines = text.split('\n')
        for line in lines:
            if '[ekspresi:' in line.lower():
                start_idx = line.lower().find('[ekspresi:') + 10
                end_idx = line.find(']', start_idx)
                if end_idx > start_idx:
                    expr = line[start_idx:end_idx].strip()
                    expressions.append(expr)
            
            if line.strip().startswith('-') and 'GERAKAN:' in text:
                movement_desc = line.strip()[1:].strip()
                if movement_desc:
                    movements.append(movement_desc)
        
        if not expressions:
            expressions = ["neutral", "happy", "surprised"]
        
        if not movements:
            movements = ["standing", "waving", "pointing"]
        
        return {
            "expressions": expressions,
            "movements": movements
        }

    def generate_image_prompt(self, script):
        prompt = f"""
        Berdasarkan script berikut, buatkan deskripsi visual untuk video:
        {script}
        
        Berikan deskripsi detail tentang:
        1. Background
        2. Warna
        3. Elemen visual
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def generate_trending_topics(self):
        prompt = "Berikan 5 topik trending di TikTok Indonesia saat ini"
        response = self.model.generate_content(prompt)
        return response.text
    
    def generate_video_ideas(self, topic):
        prompt = f"""
        Buat 3 ide video TikTok untuk topik: {topic}
        Format output:
        1. Judul:
           Script:
           Visual:
           Hashtag:
        """
        response = self.model.generate_content(prompt)
        return response.text
    
    def generate_complete_content(self):
        topics = self.generate_trending_topics()
        
        import random
        topic_list = topics.split('\n')
        selected_topic = random.choice(topic_list)
        video_content = self.generate_video_ideas(selected_topic)
        
        return {
            "topic": selected_topic,
            "content": video_content,
            "duration": 60
        }