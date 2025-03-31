from video_creator import VideoCreator
from tiktok_uploader import TikTokUploader
from content_generator import ContentGenerator
import os

class AutomaticContentCreator:
    def __init__(self, tiktok_credentials):
        self.content_generator = ContentGenerator()
        self.video_creator = VideoCreator()
        self.tiktok_uploader = TikTokUploader(tiktok_credentials)

    def create_and_upload_video(self):
        try:
            content = self.content_generator.generate_content()
            
            video_path = self.video_creator.create_video(content)
            
            if video_path and os.path.exists(video_path):
                self.tiktok_uploader.upload(video_path)
            else:
                raise Exception("Video file tidak ditemukan")
                
        except Exception as e:
            print(f"Error dalam proses: {str(e)}")
            raise