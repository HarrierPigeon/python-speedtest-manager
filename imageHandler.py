import csv
import os
import socket
import requests
import re
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import matplotlib
import functools
import io
import urllib
import config
# from io import BytesIO
relativePath = config.local_baseDir
outputFile = config.outputCSVfile
csvFilePath = os.path.join(relativePath,config.local_CSVfolder,config.outputCSVfile)
outputImagePath = os.path.join(config.local_baseDir,config.local_IMGfolder)

DEBUGSTUFF = True

# yay decorators! This was pulled from stackoverflow, should reduce runtimes after the first run by caching the font.

@functools.lru_cache
def get_font_from_url(font_url):
    return urllib.request.urlopen(font_url).read()

# fontLocation = 'totallyNotPiratedFont.ttf'
# totallyNotKindaUnintentionallyPiratedDontStealThatsWrongURL = config.FontURL

def webfont(font_url):
    return io.BytesIO(get_font_from_url(font_url))

# with webfont(totallyNotKindaUnintentionallyPiratedDontStealThatsWrongURL) as f:
#     imgfnt = ImageFont.truetype(f, 30)

def getFont(fontURL:str):
    with webfont(config.fontURL) as f:
        font = ImageFont.truetype(f, 25)
    return font


# Values pulled using MS Paint.
# darker purple background, RGB value:  27.28,48
# lighter purple background, RGB value: 38,40,59
# text color: 145,146,168
# Text we want to replace goes from 405,315 (L,H) to 550,340 (L,H)

# if we want to get rid of the ISP as well, text will go from 70,315 (L,H) to 370,340 max



lightPurpleBackground=(38, 40, 59)
darkPurpleBackground=(27,28,48)
textColor=(145,146,168)


def getImage(csvFileLocation:str,relativePath:str,imageSubDir:str,printDebug:bool):
    '''de-spaghet'd PullImage'''

    imageURLs = []
    timestamps = []
    # os.path.join(relativePath,config.local_CSVfolder,config.outputFile)
    with open(csvFileLocation) as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            # print(lines[4])
            imageURLs.append(lines[9])
            timestamps.append(lines[4])

    if printDebug == True: print(imageURLs,"\n lastest image:",imageURLs[-1])
    
    fixedTimestamp = re.sub(":","_",timestamps[-1])[0:19]

    imagePath = fixedTimestamp+"-"+socket.gethostname()+".png"
    
    imageURL = imageURLs[-1]
    imageRequest = requests.get(imageURL)

    with open(os.path.join(relativePath,imageSubDir,imagePath),"wb") as fileData:
        fileData.write(imageRequest.content)
    
    return imagePath








def modifyImage(relativePath:str,imageSubDir:str,inputImageLocation:str,replaceLocation:bool,replaceISP:bool,locationText:str,ISPtext:str,fontURL):
    imgfnt = getFont(fontURL)
    os.chdir(relativePath)
    os.chdir(imageSubDir)
    modifiedImage = Image.open(inputImageLocation)
    if DEBUGSTUFF == True: print(modifiedImage.format)
    if DEBUGSTUFF == True: print(modifiedImage.mode)
    if DEBUGSTUFF == True: print(modifiedImage.size)

    imageDrawing = ImageDraw.Draw(modifiedImage)
    if replaceLocation == True:
        imageDrawing.rectangle((405, 315, 720, 340), fill=lightPurpleBackground, outline=lightPurpleBackground)
        imageDrawing.text((406,316),locationText,font=imgfnt, fill=textColor)
    if replaceISP == True:
        imageDrawing.rectangle((70, 315, 370, 340), fill=lightPurpleBackground, outline=lightPurpleBackground)
        imageDrawing.text((73,316),ISPtext,font=imgfnt, fill=textColor)
    
    if not os.path.isdir(outputImagePath):
        os.mkdir(outputImagePath)
    
    modifiedImage.save(os.path.join(outputImagePath,config.imagePrepend+inputImageLocation))
    return modifiedImage,os.path.join(outputImagePath,config.imagePrepend+inputImageLocation)





