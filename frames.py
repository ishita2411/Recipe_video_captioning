from datetime import timedelta
import cv2
import numpy as np
import os
import json
from scipy import spatial
from collections import defaultdict
import random
def format_timedelta(td):
    """Utility function to format timedelta objects in a cool way (e.g 00:00:20.05) 
    omitting microseconds and retaining milliseconds"""
    result = str(td)
    try:
        result, ms = result.split(".")
    except ValueError:
        return (result + ".00").replace(":", "-")
    ms = int(ms)
    ms = round(ms / 1e4)
    return f"{result}.{ms:02}".replace(":", "-")


def get_saving_frames_durations(saving_fps,json_file):
    """A function that returns the list of durations where to save the frames"""
    with open(json_file, 'r') as j:
     data = json.loads(j.read())

    data=data["results"]
    s=[]
    time_stamps=[]
    for key,value in data.items():
        newdict={}
        temp_list=[]

        for t_stamps in value:
            temp_list.append(t_stamps["timestamp"])
        
        ts=[]
        for j in temp_list:
            start=j[0]
            end=j[1]
            for dur in np.arange(start,end,1/saving_fps):
                ts.append(dur)

        ts=sorted(ts)
        newdict[key]=ts
        time_stamps.append(newdict)

    return time_stamps
    

def generate_frames(video_file,saving_frames_durations,videos_list):
    filename, _ = os.path.splitext(video_file)
    name_file=filename
    filename += "-opencv"
    image_list=[]
    # make a folder by the name of the video file
    if not os.path.isdir(filename):
        os.mkdir(filename)
    # read the video file    
    cap = cv2.VideoCapture(video_file)
    # get the FPS of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    # start the loop
    count = 0
    while True:
        is_read, frame = cap.read()
        if not is_read:
            # break out of the loop if there are no frames to read
            break
        # get the duration by dividing the frame count by the FPS
        frame_duration = count / fps
        try:
            # get the earliest duration to save
            closest_duration = saving_frames_durations[0]
        except IndexError:
            # the list is empty, all duration frames were saved
            break
        if frame_duration >= closest_duration:
            # if closest duration is less than or equals the frame duration, 
            # then save the frame
            frame_duration_formatted = format_timedelta(timedelta(seconds=frame_duration))
            image_list.append(f"frame{frame_duration_formatted}.jpg")
            cv2.imwrite(os.path.join(filename, f"frame{frame_duration_formatted}.jpg"), frame) 
            # print(filename, frame_duration_formatted, frame )
            # drop the duration spot from the list, since this duration spot is already saved
            try:
                saving_frames_durations.pop(0)
            except IndexError:
                pass
        # increment the frame count
        count += 1
    videos_list[name_file]=image_list

def get_similar_frames(videos_features_vectors,videos_list):
  result={}
  for key,value in videos_features_vectors.items():
    allVectors=value
    image_list=videos_list[key]

    img1 = allVectors[image_list[0]]

    similar_images = defaultdict(lambda: [])
    similar_images[1].append(image_list[0])
    similar_count = 1

    for i in range(1, len(image_list)):
      img2 = allVectors[image_list[i]]

      similarity = -1 * (spatial.distance.cosine(img1, img2) - 1)

      if(similarity >= 0.8):
        similar_images[similar_count].append(image_list[i])
      else:
        img1 = img2
        similar_count = similar_count + 1
        similar_images[similar_count].append(image_list[i])
    result[key]=similar_images

  return result

def get_final_frames(results):
  final_frames={}
  for key, value in results.items():
    video_frame={}
    similar_images=value
    video_frame={k:random.choice(v) for k,v in similar_images.items()}
    final_frames[key]=video_frame
  return final_frames