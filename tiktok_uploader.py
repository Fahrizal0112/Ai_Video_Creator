from TikTokApi import TikTokApi
import asyncio
import nest_asyncio

# Patch asyncio untuk menangani nested event loops
nest_asyncio.apply()

class TikTokUploader:
    def __init__(self, credentials):
        self.credentials = credentials
        self.api = None
    
    def upload(self, video_path):
        try:
            # Buat event loop baru
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            async def upload_video():
                async with TikTokApi() as api:
                    # Login
                    await api.create_sessions(
                        username=self.credentials["username"],
                        password=self.credentials["password"]
                    )
                    
                    # Upload
                    result = await api.video.upload(
                        video_path,
                        description="Video yang dibuat otomatis #viral #fyp"
                    )
                    return result
            
            # Run upload dalam event loop
            result = loop.run_until_complete(upload_video())
            loop.close()
            
            print(f"Video berhasil diupload: {result}")
            return result
            
        except Exception as e:
            print(f"Error saat upload ke TikTok: {str(e)}")
            # Simpan video tanpa upload jika error
            print(f"Video tersimpan di: {video_path}")
            return None
        finally:
            # Pastikan event loop ditutup
            try:
                loop.close()
            except:
                pass