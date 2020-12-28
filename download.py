
import time
import os
import glob
import shutil
from moviepy.editor import *
from pytube import YouTube
from argparse import ArgumentParser

def get_test_path(output_path):

      path_list = []

      for subdir, dirs, files in os.walk(output_path):
            for file in files:
                  if file.endswith(".wav"):
                        path_list.append(file.replace(".wav",""))

      return path_list

def create_dir(dir_path):
      if not os.path.exists(dir_path):
            os.makedirs(dir_path)

parser = ArgumentParser()
parser.add_argument("input",type=str)
parser.add_argument("--output_wav", default='wav',type=str)
parser.add_argument("--output_video", default='video',type=str)
parser.add_argument("--save_video", default='False')

args = parser.parse_args()

f = open(args.input)
file_info = list(f.readlines())[3:]

output_path = args.output_wav
video_output = args.output_video

create_dir(output_path)
create_dir(video_output)

f_failed = open("error_message.txt", "a+")

file_dict = {}
for line in file_info:
    info = line.split(",")
    idx = info[0]
    start = time.strftime('%H:%M:%S', time.gmtime(int(float(info[1]))))
    end = time.strftime('%H:%M:%S', time.gmtime(int(float(info[2]))))     
    file_dict[idx] = [start, end] 

exist_wav = get_test_path(output_path)
for wav in exist_wav:
      file_dict.pop(wav, None)

failed = list(f_failed.readlines())
for line in failed:
      wav = line.split("#")[0]
      file_dict.pop(wav, None)

for key, value in file_dict.items():
    idx = key
    start = file_dict[key][0]
    end = file_dict[key][1]
    print("processing:",idx)
    try:
      yt = YouTube('https://youtu.be/'+idx).streams.first().download(os.path.join(video_output,idx))
      video_path = glob.glob(os.path.join(video_output,idx,"*.mp4"))[0]
      sound = AudioFileClip(video_path)
      newsound = sound.subclip(start, end)   
      newsound.write_audiofile(os.path.join(output_path,idx+".wav"))
      if args.save_video=='False':
            shutil.rmtree(os.path.join(video_output,idx))
      print("processing OK:", idx)
    except Exception as e:
      print("processing Fail:", e, idx)
      f_failed.write(idx+"#"+str(e)+'\n')

if args.save_video=='False':
      shutil.rmtree(os.path.join(video_output))

f.close
f_failed.close
