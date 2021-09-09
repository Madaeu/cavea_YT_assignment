#!/usr/bin/python

#from __future__ import unicode_literals
import youtube_dl
import cv2 as cv
import shutil
import os

video_urls = ['https://www.youtube.com/watch?v=y8Kyi0WNg40',\
'https://www.youtube.com/watch?v=XgvR3y5JCXg',\
'https://www.youtube.com/watch?v=KmtzQCSh6xk',\
'https://www.youtube.com/watch?v=PfYnvDL0Qcw',\
'https://www.youtube.com/watch?v=HsvA7p0LYUk',\
'https://www.youtube.com/watch?v=HPPj6viIBmU',\
'https://www.youtube.com/watch?v=J---aiyznGQ',\
'https://www.youtube.com/watch?v=lrzKT-dFUjE',\
'https://www.youtube.com/watch?v=QH2-TGUlwu4',\
'https://www.youtube.com/watch?v=YBkmefllgiE',\
'https://www.youtube.com/watch?v=gNgXP4HII_4',\
'https://www.youtube.com/watch?v=EIyixC9NsLI',\
'https://www.youtube.com/watch?v=P5ex69c_dAs']

# Path variables
current_path = os.getcwd()
temp_video_path = current_path + '/temp_video'
video_path = current_path + '/video'

# Create temporary directory for downloaded videos for easier and safe removal
try:
    os.mkdir(temp_video_path)
except OSError as error:
    print(error)


# Download videos (id and extension) to temporary video directory
ydl_opts = {'outtmpl': temp_video_path + '/%(id)s.%(ext)s'}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(video_urls)

# Iterate through the downloaded videos in temp directory
with os.scandir(temp_video_path) as entries:
    for entry in entries:
        if entry.is_file:
            
            video_name = entry.name.rsplit('.', 1)[0]
            folder_path = video_path + '/' + video_name
            
            # Create frame folder using video ID
            try:
                os.makedirs(folder_path)
            except OSError as error:
                print(error)
            
            # Open video
            video_cap = cv.VideoCapture(entry.path)
            if (video_cap.isOpened()==False):
                print('Error opening video file %s!' % entry.path)
            
            seconds = 0
            hasFrame = True

            while hasFrame == True:
                # Extract frame at n'th second
                video_cap.set(cv.CAP_PROP_POS_MSEC, seconds*1000)
                hasFrame, frame = video_cap.read()

                if hasFrame == True:
                    # Save frame in corresponding folder
                    cv.imwrite(folder_path + '/' + video_name + '_' + str(seconds) + '.png', frame)
                    seconds = seconds+1

try:
    print('Removing temporary video directory')
    shutil.rmtree(temp_video_path)
except OSError as error:
    print(error)



            
            
