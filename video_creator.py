import moviepy.editor as mpy
from gtts import gTTS
import os
from dotenv import load_dotenv
import requests
from PIL import Image
from io import BytesIO
import numpy as np
from moviepy.video.tools.segmenting import findObjects

# Load environment variables
load_dotenv()

output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

class VideoCreator:
    def __init__(self):
        self.hf_api_key = os.getenv('HUGGINGFACE_API_KEY')
        if not self.hf_api_key:
            raise ValueError("HUGGINGFACE_API_KEY tidak ditemukan di file .env")
    
    def resize_image(self, image, size):
        """Helper function untuk resize image dengan method yang benar"""
        return image.resize(size, Image.Resampling.LANCZOS)
    
    def generate_character_frames(self, expressions):
        frames = []
        for expr in expressions:
            try:
                API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
                headers = {"Authorization": f"Bearer {self.hf_api_key}"}
                
                response = requests.post(
                    API_URL,
                    headers=headers,
                    json={"inputs": f"cartoon character, {expr} expression, full body, centered"}
                )
                
                if response.status_code == 200:
                    frame = Image.open(BytesIO(response.content))
                    frames.append(frame)
                else:
                    frames.append(self.get_placeholder_image())
                    
            except Exception as e:
                print(f"Error generating frame for {expr}: {str(e)}")
                frames.append(self.get_placeholder_image())
        
        return frames

    def create_animated_character(self, frames, duration):
        frame_clips = []
        frame_duration = duration / len(frames)
        
        for i, frame in enumerate(frames):
            # Simpan frame
            frame_path = os.path.join(output_dir, f"frame_{i}.png")
            
            # Resize frame
            new_height = 600
            aspect_ratio = frame.size[0] / frame.size[1]
            new_width = int(new_height * aspect_ratio)
            resized_frame = frame.resize((new_width, new_height), Image.Resampling.LANCZOS)
            resized_frame.save(frame_path, quality=95)
            
            # Buat clip
            clip = mpy.ImageClip(frame_path)
            
            # Tambah efek gerak
            clip = (clip
                   .set_duration(frame_duration)
                   .set_position(lambda t: (
                       "center",
                       800 + np.sin(t*2)*20  # Gerakan naik turun
                   )))
            
            # Tambah efek rotasi untuk frame tertentu
            if i % 2 == 0:
                clip = clip.rotate(lambda t: np.sin(t*2)*5)  # Rotasi kecil
            
            frame_clips.append(clip)
        
        # Gabungkan frame dengan transisi
        character = mpy.concatenate_videoclips(
            frame_clips,
            method="compose"
        )
        
        return character

    def create_video(self, content):
        try:
            script_data = self.parse_script(content["script"])
            
            # Generate audio
            audio_path = os.path.join(output_dir, "audio.mp3")
            tts = gTTS(text=script_data["dialog"], lang='id')
            tts.save(audio_path)
            
            audio = mpy.AudioFileClip(audio_path)
            
            # Generate character frames
            print("Generating character frames...")
            expressions = [
                "neutral", "happy", "excited", 
                "surprised", "laughing"
            ]
            frames = self.generate_character_frames(expressions)
            
            # Create video elements
            print("Creating video elements...")
            bg = mpy.ColorClip(size=(1080, 1920), color=[20, 20, 20])
            bg = bg.set_duration(audio.duration)
            
            # Create animated character
            character = self.create_animated_character(frames, audio.duration)
            
            # Add animated text dengan efek bounce
            txt_clip = (mpy.TextClip(
                script_data["dialog"],
                fontsize=70,
                color='white',
                size=(1000, 1800),
                method='caption',
                stroke_color='black',
                stroke_width=2
            )
            .set_duration(audio.duration)
            .set_position(lambda t: (
                "center",
                400 + np.sin(t*1.5)*10  # Text bergerak naik turun
            )))
            
            # Combine elements dengan efek
            final = mpy.CompositeVideoClip([
                bg,
                character,
                txt_clip
            ])
            final = final.set_audio(audio)
            
            # Export dengan kualitas tinggi
            print("Exporting video...")
            output_path = os.path.join(output_dir, "output_video.mp4")
            final.write_videofile(
                output_path,
                fps=30,
                codec='libx264',
                audio_codec='aac',
                threads=4,
                preset='medium'
            )
            
            # Cleanup
            self.cleanup_temp_files(audio_path)
            
            return output_path
            
        except Exception as e:
            print(f"Error dalam pembuatan video: {str(e)}")
            raise

    def cleanup_temp_files(self, audio_path):
        # Hapus file temporary
        os.remove(audio_path)
        for file in os.listdir(output_dir):
            if file.startswith("frame_") and file.endswith(".png"):
                os.remove(os.path.join(output_dir, file))

    def get_placeholder_image(self):
        # Buat gambar placeholder putih
        return Image.new('RGB', (512, 512), color='white')
    
    def parse_script(self, script_text):
        try:
            result = {
                "dialog": "",
                "expressions": ["neutral"],
                "sound_effects": []
            }
            
            lines = script_text.split('\n')
            dialog_parts = []
            is_dialog_section = False
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                if "DIALOG:" in line:
                    is_dialog_section = True
                    continue
                elif "SOUND_EFFECT:" in line:
                    is_dialog_section = False
                    effects = line.replace("SOUND_EFFECT:", "").strip()
                    result["sound_effects"] = [e.strip() for e in effects.split(',')]
                elif is_dialog_section and line:
                    dialog_text = line.split('[')[0].strip()
                    dialog_parts.append(dialog_text)
            
            result["dialog"] = " ".join(dialog_parts)
            
            if not result["dialog"]:
                raise ValueError("Tidak ada dialog yang bisa diproses")
                
            return result
            
        except Exception as e:
            print(f"Error dalam parsing script: {str(e)}")
            raise