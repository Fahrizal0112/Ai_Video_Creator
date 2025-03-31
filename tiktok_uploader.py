
from TikTokApi import TikTokApi

class TikTokUploader:
    def __init__(self, credentials):
        self.api = TikTokApi()
        self.credentials = credentials
    
    def upload(self, video_path):
        # Login ke TikTok
        self.api.login(username=self.credentials["username"],
                      password=self.credentials["password"])
        
        # Upload video
        self.api.upload_video(video_path,
                            description="Video yang dibuat otomatis #viral #fyp")