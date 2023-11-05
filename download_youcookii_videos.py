# Script for downloading youcookii videos
# Written by Luowei Zhou, 09/23/2017
# Contact luozhou@umich.edu if you have trouble downloading some private/unavailable videos

# Requirement: install youtube-dl (https://github.com/rg3/youtube-dl/)

import os
pwd=os.getcwd()
dataset_root = pwd
vid_file_lst = [f'{pwd}/trial.txt']
split_lst = ['training', 'validation', 'testing']
if not os.path.isdir(dataset_root):
    os.mkdir(dataset_root)

missing_vid_lst = []

# download videos for training/validation/testing splits
for vid_file in vid_file_lst:
    if not os.path.isdir(os.path.join(dataset_root)):
        os.mkdir(os.path.join(dataset_root))
    with open(vid_file) as f:
        lines = f.readlines()
        for line in lines:
            
            vid_name = line.replace('\n','')
            if not os.path.isdir(os.path.join(dataset_root)):
                os.mkdir(os.path.join(dataset_root))

            # download the video
            vid_url = 'www.youtube.com/watch?v='+vid_name
            vid_prefix = os.path.join(dataset_root, vid_name) 
            os.system(' '.join(("yt-dlp -o", vid_prefix, vid_url)))

            # check if the video is downloaded
            if os.path.exists(vid_prefix+'.mp4') or os.path.exists(vid_prefix+'.mkv') or os.path.exists(vid_prefix+'.webm'):
                print('[INFO] Downloaded video {}'.format(vid_name))
            else:
                missing_vid_lst.append('/'.join(line))
                print('[INFO] Cannot download video {}'.format( vid_name))

# write the missing videos to file
missing_vid = open('missing_videos.txt', 'w')
for line in missing_vid_lst:
    missing_vid.write(line)

# sanitize and remove the intermediate files
# os.system("find ../raw_videos -name '*.part*' -delete")
os.system("find ../raw_videos -name '*.f*' -delete")
