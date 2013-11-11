'''
Created on Nov 2, 2012

@author: larson
'''
import os
import sys
import getopt
import subprocess
import time
import random
import threading

def playSong(songList,path):
    #print(songPath)
    for iRange in range(60):
        songPath = random.choice(songList)
        duration = int(getDuration(songPath));
        songList.remove(songPath)
        startTime = random.uniform(10,duration - 70)
        threading.Timer(60.2,playSong,[songList,path]).start()
        p = subprocess.call([path,"--fullscreen","--play-and-exit","--start-time",str(startTime),"--stop-time",str(startTime + 60),"--run-time",str(60),songPath])
    
def getDuration(songPath):
    ffmpeg = subprocess.Popen(['/Users/larson/Development/random-hour/src/ffmpeg','-i',songPath], stderr=subprocess.STDOUT,stdout = subprocess.PIPE )
    out,err = ffmpeg.communicate()
    fileLength = ''
    if "Duration" in out:
        fileLength = out[out.index("Duration"):].split()[1]
    fileLength = fileLength[:-4]
    return getSec(fileLength)

def getSec(s):
    l = s.split(':')
    return str(int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2]))

def main(argv):
    #--start-time=<int>
    #--run-time=60
    directory = "/Users/larson/Documents/ph4"
    vlcpath = "/Applications/VLC.app/Contents/MacOS/VLC"
    numSongs = 60
    try:
        opts,args = getopt.getopt(argv, "hd:p:n:", ["directory=","vlcpath=","numSongs="])
    except getopt.GetoptError:
        print("randomhour.py -d <video file directory> -p <vlc path> -n <number of songs>")
        sys.exit(2)
    for opt,arg in opts:
        if opt == "-h":
            print("randomhour.py -d <video file directory> -p <vlc path> -n <number of songs>")
            sys.exit()
        elif opt in ("-d","--directory"):
            directory = arg
        elif opt in ("-p","--vlcpath"):
            vlcpath = arg
        elif opt in ("-n","--numSongs"):
            numSongs = arg
    print("directory:" + directory + ", vlcpath:" + vlcpath)
    fullDirs = []
    dirList = os.listdir(directory)
    for fName in dirList:
        if fName != ".DS_Store":
            fullDirs.append(directory + "/" + fName)
    
    playSong(fullDirs,vlcpath)
    
if __name__ == '__main__':
    main(sys.argv[1:])
