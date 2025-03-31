import moviepy.editor as mpy
from gtts import gTTS
import os
from diffusers import StableDiffusionPipeline
import torch
from moviepy.config import change_settings
from bark import SAMPLE_RATE, generate_audio, preload_models
import numpy as np
from scipy.io.wavfile import write as write_wav

output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

class VideoCreator:
    def __init__(self):
        try:
            if torch.backends.mps.is_available():
                device = "mps"
            else:
                device = "cpu"
            
            self.pipe = StableDiffusionPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5",
                torch_dtype=torch.float32
            )
            self.pipe = self.pipe.to(device)
            
            self.pipe.enable_attention_slicing()
        except Exception as e:
            print(f"Error saat inisialisasi VideoCreator: {str(e)}")
            raise
    
    def load_bark_models(self):
        # Set environment variable untuk torch.load
        os.environ['TORCH_LOAD_WEIGHTS_ONLY'] = '0'
        
        # Preload models dengan konfigurasi yang benar
        preload_models()
    
    def generate_character_frame(self, expression, pose):
        prompt = f"""
        cartoon character, {expression} expression, {pose},
        cute anime style, high quality, simple background,
        full body shot, centered
        """
        
        image = self.pipe(prompt).images[0]
        return image
    
    def generate_audio_bark(self, text, voice_preset="male_funny"):
        try:
            audio_array = generate_audio(
                text,
                history_prompt=self.voice_presets[voice_preset],
                text_temp=0.7,
                waveform_temp=0.7
            )
            
            audio_path = os.path.join("output", "generated_audio.wav")
            write_wav(audio_path, SAMPLE_RATE, audio_array)
            
            return audio_path
            
        except Exception as e:
            print(f"Error dalam generate audio: {str(e)}")
            return None
    
    def create_video(self, content):
        try:
            script_data = self.parse_script(content["script"])
            
            # Generate audio dengan gTTS
            audio_path = os.path.join(output_dir, "audio.mp3")
            tts = gTTS(text=script_data["dialog"], lang='id')
            tts.save(audio_path)
            
            audio = mpy.AudioFileClip(audio_path)
            
            # Generate character frame
            character_image = self.generate_character_frame("neutral", "standing")
            character_path = os.path.join(output_dir, "character.png")
            character_image.save(character_path)
            
            # Create video elements
            bg = mpy.ColorClip(size=(1080, 1920), color=[20, 20, 20])
            bg = bg.set_duration(audio.duration)
            
            character = mpy.ImageClip(character_path)
            character = character.set_duration(audio.duration)
            character = character.resize(height=600)
            character = character.set_position(("center", 800))
            
            # Add text
            txt_clip = mpy.TextClip(
                script_data["dialog"],
                fontsize=70,
                color='white',
                size=(1000, 1800),
                method='caption'
            )
            txt_clip = txt_clip.set_duration(audio.duration)
            txt_clip = txt_clip.set_position(("center", 400))
            
            # Combine all elements
            final = mpy.CompositeVideoClip([
                bg,
                character,
                txt_clip
            ])
            final = final.set_audio(audio)
            
            # Export
            output_path = os.path.join(output_dir, "output_video.mp4")
            final.write_videofile(
                output_path,
                fps=30,
                codec='libx264',
                audio_codec='aac'
            )
            
            # Cleanup temporary files
            os.remove(audio_path)
            os.remove(character_path)
            
            return output_path
            
        except Exception as e:
            print(f"Error dalam pembuatan video: {str(e)}")
            raise
    
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