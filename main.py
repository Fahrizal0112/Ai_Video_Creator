from video_creator import VideoCreator
from tiktok_uploader import TiktokUploader
from content_generator import ContentGenerator

class AutomaticContentCreator:
    def __init__(self, tiktok_credentials):
        self.content_generator = ContentGenerator()
        self.video_creator = VideoCreator()
        self.tiktok_uploader = TiktokUploader(tiktok_credentials)

    def create_and_upload_video(self):
        content = self.content_generator.generate_content()
        video_path = self.video_creator.create_video(content)
        self.tiktok_uploader.upload_video(video_path)