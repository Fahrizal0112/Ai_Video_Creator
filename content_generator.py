import google.generativeai as genai
import time
from tenacity import retry, stop_after_attempt, wait_exponential

class ContentGenerator:
    def __init__(self):
        genai.configure(api_key="AIzaSyAB4o8VpccbEeM_jlCOIezJGYRDoA488Ig")
        self.model = genai.GenerativeModel('gemini-2.5-pro-exp-03-25')
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def generate_content(self):
        try:
            prompt = """
            Buatkan script video TikTok lucu dengan durasi 30 detik.
            Format output HARUS seperti ini dan dialog HARUS lebih dari 5 kalimat:
            
            KARAKTER: Cowok Gen-Z dengan ekspresi berlebihan, rambut berantakan
            MOOD: Energetic dan kocak
            SETTING: Kamar dengan poster anime
            
            DIALOG:
            - "Waduh gaes! Gak nyangka hari ini..." [ekspresi: excited]
            - "Kalian tau gak sih, tadi pagi gue..." [ekspresi: storytelling]
            - "Terus pas di jalan tuh ya..." [ekspresi: dramatic]
            - "Eh tau-tau ada yang..." [ekspresi: surprised]
            - "Yang bikin gue kaget tuh..." [ekspresi: shocked]
            - "Akhirnya gue..." [ekspresi: relief]
            - "Pokoknya intinya gaes..." [ekspresi: laughing]
            - "Jangan lupa like, share, comment ya!" [ekspresi: happy]
            
            SOUND_EFFECT: laugh, boom, ding, wow
            
            HASHTAG: #viral #comedy #lucu #trending #fyp
            
            Note: Buat cerita yang mengalir dan lucu, dengan twist di tengah cerita.
            """
            
            response = self.model.generate_content(prompt)
            
            if not response.text or len(response.text.split('\n')) < 10:
                return {
                    "script": """
                    KARAKTER: Cowok Gen-Z dengan rambut berantakan
                    MOOD: Super energetic
                    SETTING: Kamar gaming setup
                    
                    DIALOG:
                    - "Waduh gaes! Gak nyangka hari ini gue bakal cerita hal gokil!" [ekspresi: excited]
                    - "Jadi tadi pagi ya, gue bangun kesiangan seperti biasa..." [ekspresi: storytelling]
                    - "Pas lagi buru-buru, eh malah kepeleset kulit pisang!" [ekspresi: dramatic]
                    - "Tapi yang bikin kocak, ternyata..." [ekspresi: buildup]
                    - "Ada tetangga yang ngerekam, langsung viral dong!" [ekspresi: laughing]
                    - "Sekarang followers TikTok gue nambah 10 ribu!" [ekspresi: shocked]
                    - "Moral of the story: kadang kesialan bisa jadi berkah" [ekspresi: wise]
                    - "Makanya jangan lupa follow gue ya gaes!" [ekspresi: happy]
                    
                    SOUND_EFFECT: laugh, boom, ding, wow, applause
                    
                    HASHTAG: #viral #comedy #lucu #trending #fyp
                    """,
                    "duration": 30,
                    "style": "comedy"
                }
            
            return {
                "script": response.text,
                "duration": 30,
                "style": "comedy"
            }
            
        except Exception as e:
            print(f"Error generating content: {str(e)}")
            return {
                "script": """
                KARAKTER: Cowok Gen-Z dengan rambut berantakan
                MOOD: Super energetic
                SETTING: Kamar gaming setup
                
                DIALOG:
                - "Waduh gaes! Gak nyangka hari ini gue bakal cerita hal gokil!" [ekspresi: excited]
                - "Jadi tadi pagi ya, gue bangun kesiangan seperti biasa..." [ekspresi: storytelling]
                - "Pas lagi buru-buru, eh malah kepeleset kulit pisang!" [ekspresi: dramatic]
                - "Tapi yang bikin kocak, ternyata..." [ekspresi: buildup]
                - "Ada tetangga yang ngerekam, langsung viral dong!" [ekspresi: laughing]
                - "Sekarang followers TikTok gue nambah 10 ribu!" [ekspresi: shocked]
                - "Moral of the story: kadang kesialan bisa jadi berkah" [ekspresi: wise]
                - "Makanya jangan lupa follow gue ya gaes!" [ekspresi: happy]
                
                SOUND_EFFECT: laugh, boom, ding, wow, applause
                
                HASHTAG: #viral #comedy #lucu #trending #fyp
                """,
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