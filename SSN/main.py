from GUI import GUI
from RoadNetwork import RoadNetwork
from SocialNetwork import SocialNetwork
import os
import tkinter as tk
import time
import threading
import urllib.request
import zipfile
import numpy as np


rPath = "dataSets\\roadMaps\\"
sPath = "dataSets\\socialNetworks\\"
california = None
gowalla, tweets, weibo, foursquare = None, None, None, None


def initCalifornia():
    global california
    california = RoadNetwork('California', f"{rPath}cal.cnode.npy", f"{rPath}cal.cedge.npy",
                             f"{rPath}california_Lat.npy", f"{rPath}california_Long.npy")


def initGowalla():
    global gowalla
    gowalla = SocialNetwork('gowalla', f"{sPath}gowalla_loc.json", f"{sPath}gowalla_rel.json", f"gowalla_Keywords.npy")


def initTweets():
    global tweets
    tweets = SocialNetwork('tweets', f"{sPath}tweets_loc.json", f"{sPath}tweets_rel.json", '')


def initWeibo():
    global weibo
    weibo = SocialNetwork('weibo', f"{sPath}weibo_loc.json", f"{sPath}weibo_rel.json", '')


def initFoursquare():
    global foursquare
    foursquare = SocialNetwork('foursquare', f"{sPath}foursquare_loc.json", f"{sPath}foursquare_rel.json", '')


# Initializes RoadNetworks from datasets
def initRoadNetworks():
    print("Initializing road network")
    timer = time.perf_counter()
    networkThread = threading.Thread(target=initCalifornia)
    networkThread.start()
    networkThread.join()
    print(f"Done initializing road maps. Task took {round(time.perf_counter() - timer, 6)} seconds.")


# Initializes SocialNetworks from datasets
def initSocialNetworks():
    print("Initializing social network")
    timer = time.perf_counter()
    networkThreads = [threading.Thread(target=initGowalla), threading.Thread(target=initTweets),
                      threading.Thread(target=initWeibo), threading.Thread(target=initFoursquare)]
    for thread in networkThreads:
        thread.start()
    for thread in networkThreads:
        thread.join()
    print(f"Done initializing social maps. Task took {round(time.perf_counter() - timer, 6)} seconds.")


# Downloads road map datasets
def getRoadMapDatasets():
    print("Road network datasets not detected. Downloading...")
    try:
        os.mkdir(rPath)
        urllib.request.urlretrieve("https://dl.dropboxusercontent.com/s/jh9vwcn2nh875w2/roadMaps.zip?dl=0",
                                   f"{rPath}roadDatasets.zip")
        with zipfile.ZipFile(f"{rPath}roadDatasets.zip", 'r') as zip_ref:
            zip_ref.extractall(rPath)
        os.remove(f"{rPath}roadDatasets.zip")
        print("Done downloading road network datasets.")
    except:
        print("ERROR: Something went wrong when downloading the road map datasets. Please check your internet\n"
              f"connection or download the files manually from https://dl.dropboxusercontent.com/s/jh9vwcn2nh875w2/roadMaps.zip?dl=0\n"
              f"and unzip the file to dir {rPath}.")


# Downloads social network datasets
def getSocialNetworkDatasets():
    print("Social network datasets not detected. Downloading...")
    try:
        os.mkdir(sPath)
        urllib.request.urlretrieve("https://srv-store1.gofile.io/download/0UQyaZ/77399a3122d32877cfb8d5790c434d85/socialNetworks.zip",
                                   f"{sPath}socialDatasets.zip")
        with zipfile.ZipFile(f"{sPath}socialDatasets.zip", 'r') as zip_ref:
            zip_ref.extractall(sPath)
        os.remove(f"{sPath}socialDatasets.zip")
        print("Done downloading social network datasets.")
    except:
        print("ERROR: Something went wrong when downloading the social network datasets. Please check your internet\n"
              f"connection or download the files manually from https://srv-store1.gofile.io/download/0UQyaZ/77399a3122d32877cfb8d5790c434d85/socialNetworks.zip\n"
              f"and unzip the file to dir {rPath}.")


print("--- Initialization Started")
timer = time.perf_counter()
downloadThreads = []
initThreads = [threading.Thread(target=initRoadNetworks), threading.Thread(target=initSocialNetworks)]
if not os.path.isdir(rPath):
    downloadThreads.append(threading.Thread(target=getRoadMapDatasets))
if not os.path.isdir(sPath):
    downloadThreads.append(threading.Thread(target=getSocialNetworkDatasets))
for thread in downloadThreads:
    thread.start()
for thread in downloadThreads:
    thread.join()
for thread in initThreads:
    thread.start()
for thread in initThreads:
    thread.join()
print(f"--- Initializing done. Task took {round((time.perf_counter() - timer), 6)} seconds")

print(f"GUI opening")
root = tk.Tk()
gui = GUI(master=root)
gui.defMap(california, 'california')
gui.defSoc(gowalla, 'gowalla', '#03fc24')
gui.defSoc(tweets, 'tweets', '#5e69ff')
gui.defSoc(weibo, 'weibo', '#b750c7')
gui.defSoc(foursquare, 'foursquare', '#ffc124')
gui.mainloop()
