from pathlib import Path
from gtts import gTTS
from moviepy.editor import *
import random

quotes = []

value = "-"
time = 1

imagePath = Path.cwd() / "Images"
audioPath = Path.cwd() / "Audio"
outputPath = Path.cwd() / "Output"

if(not (imagePath.exists() and audioPath.exists() and outputPath.exists())):
    imagePath.mkdir(exist_ok=True)
    audioPath.mkdir(exist_ok=True)
    outputPath.mkdir(exist_ok=True)
    print("[NOTE] The folders are created. Restart the program.")
    quit()

print("[NOTE] If you want to continue, just type enter with nothing in the input.")

while value != "" or len(quotes) <= 0:
    value = input(f"{time}: ")
    
    if value != "":
        image = input(f"Image : ")
        
        if(not (imagePath / image).exists() or len(image) == 0):
            print(f"[WARN] The image doesn't exist.")
            continue
        
        quotes.append([value, image])
        print("[NOTE] Values added to the list.")    
    
    if len(quotes) > 0:
        time += 1
    else:
        print("[WARN] There is no quote and no image.")

width = ""
height = ""

while not(width.isdigit() and height.isdigit()):
    width = input(f"Width of the video : ")
    height = input(f"Height of the video : ")
    
    if not(width.isdigit() and height.isdigit()):
        print("[WARN] Please enter numbers.")

width = int(width)
height = int(height)

name = input("Name of the video : ")

if len(name) <= 0:
    name = str(random.randint(10000000000000,99999999999999)) + ".mp4"
else:
    name += ".mp4"

frames_per_second = input("The number of FPS : ")

if frames_per_second.isdigit():
    frames_per_second = int(frames_per_second)
else:
    frames_per_second = 30

background_red = 255
background_green = 255
background_blue = 255

print("The color of the background :")

background_red = input(" - RED : ")

if background_red.isdigit():
    background_red = int(background_red)
    background_red = 255 if background_red > 255 else background_red
    background_red = 0 if background_red < 0 else background_red
else:
    background_red = 255

background_green = input(" - GREEN : ")

if background_green.isdigit():
    background_green = int(background_green)
    background_green = 255 if background_green > 255 else background_green
    background_green = 0 if background_green < 0 else background_green
else:
    background_green = 255

background_blue = input(" - BLUE : ")

if background_blue.isdigit():
    background_blue = int(background_blue)
    background_blue = 255 if background_blue > 255 else background_blue 
    background_blue = 0 if background_blue < 0 else background_blue
else:
    background_blue = 255

time = 0

print("[NOTE] Creation of the audio files.")

for i in quotes:
    tts = gTTS(i[0])
    tts.save(str(audioPath / f"{time}.mp3"))
    print(f"[PROCESSING] {time}.mp3 is created.")
    time += 1

print("[NOTE] The audio files are created.")

time = 0

clips = []

print("[NOTE] Creation of the clips.")

for i in quotes:
    audio = AudioFileClip(str(audioPath / f"{time}.mp3"))

    clip = ImageClip(str(imagePath / i[1])).set_duration(audio.duration)
    clip = clip.set_audio(audio)
    clip = clip.set_position(("center"))
    clip = clip.resize(width=width - (width // 15))
    
    clipheight = clip.h
    
    while clip.h > round(clipheight * 0.95):
        clip = clip.resize(width=(clip.w-5))
    
    if time > 0:
        clip = clip.set_start(clips[time - 1].end)
    
    print(f"[PROCESSING] Clip {time} is created. (width:{clip.w}, height:{clip.h}, position:center, duration:{clip.duration}, start:{clip.start})")
    
    clips.append(clip)

    time += 1

print("[NOTE] The clips are created.")
print("[NOTE] Creation of the final clip.")

assemblate_clip = CompositeVideoClip(clips, size=(width,height))
assemblate_clip = assemblate_clip.set_position("center")

color_clip = ColorClip(size = (width, height), color = [background_red, background_green, background_blue])
color_clip = color_clip.set_duration(assemblate_clip.duration)

final_clip = CompositeVideoClip([color_clip, assemblate_clip], size=(width,height))
final_clip.write_videofile(str(outputPath / name), fps=frames_per_second)

print(f"[NOTE] Your video is created. (width:{final_clip.w}, height:{final_clip.h}, duration:{final_clip.duration}, start:{final_clip.start}, fps:{frames_per_second}, name:{name})")

print(f"[NOTE] Deleting all audio files.")

for f in audioPath.iterdir():
    if f.is_file():
        f.unlink()
    
    print(f"[PROCESSING] {f.name} is deleted.")

print(f"[NOTE] The audio files are deleted.")