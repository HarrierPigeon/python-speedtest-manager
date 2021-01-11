import subprocess
import socket
import csv
import os
import secrets
import FTPhandler
import matplotlib
import config
import imageHandler
import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# This code has a TON of print statements in here from when I was writing and debugging the thing- 
# instead of remove them outright, I've added "flags" for them in config- to get a *bunch* of data, set enableTonsOfPrintInfo to True.
# There's also an optional "running speedtest" message in case you want to know if that worked or not.


# hostnasme = socket.gethostname()
# This program creates a separate file per-hostname, because KIS,S.  Can join in Excel / etc. easily enough.


if config.enableTonsOfPrintInfo == True: print("config.outputCSVfile: ",config.outputCSVfile) 
if config.enableTonsOfPrintInfo == True: print("outputCSVfilePath: ",os.path.join(config.local_baseDir,config.local_CSVfolder,config.outputCSVfile)) 


if config.enableTonsOfPrintInfo == True: print("running")

 

def getSpeedtestResults():
    '''requires speedtest-cli from pip.  Thanks for the tool, speedtest.net!'''
    result = subprocess.run(['speedtest-cli','--csv','--share'],stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    if config.enableTonsOfPrintInfo == True: print(output)
    return output

# At this point, results have a weird \r\n at the end that simply won't do, so the next function cleans that up and adds the computer's hostname to it as well.


def formatResults(input1: str):
    '''adds hostname to the beginning and removes the \r\n from the end''' 
    output = socket.gethostname() + "," + input1.rstrip('\r\n')
    # This part removes a T and a Z so that the time goes from "2021-01-07T16:01:22.412761Z" to "2021-01-07 16:01:22.41276".
    # Makes it possible to parse as Date Time in Google Sheets (and others, I'd wager) directly without needing to parse data manually first.
    output = output[:51]+" "+output[52:66]+output[68:] 
    if config.enableTonsOfPrintInfo == True: print(output)
    return output

# Result CSV headers:
#'Hostname,Server ID,Sponsor,Server Name,Timestamp,Distance,Ping,Download,Upload,Share,IP Address'
# to see what these are for yourself, run ``speedtest-cli --csv-header``.  I added the hostname to the front for organizational purposes.
# csvHeader = 'Hostname,Server ID,Sponsor,Server Name,Timestamp,Distance,Ping,Download,Upload,Share,IP Address'
csvHeaders = ['Hostname', 'Server ID', 'Sponsor', 'Server Name', 'Timestamp', 'Distance', 'Ping', 'Download', 'Upload', 'Share', 'IP Address']

# if config.enableTonsOfPrintInfo == True: print(formattingTest.split(','))

def outputAsList(input1):
    '''turns comma-delimited lines into a list for more proper storage or something like that.'''
    output = []
    for line in csv.reader([input1],skipinitialspace=True):
        output += line
    return output

# if config.enableTonsOfPrintInfo == True: print(outputAsList(formattingTest))


# courtesy of https://stackoverflow.com/a/37256114

class cantAccessException(Exception):
    pass

def canAccess(targetFile):
    '''simple enough, tries to rename a file to the name it already has to see if there's access or not.  WILL throw a (custom, ooh!) error if it can't obtain write access.'''
    if os.path.isfile(targetFile):
        try:
            os.rename(targetFile, targetFile)
            if config.enableTonsOfPrintInfo == True: print('Access on file "' + targetFile +'" is available!')
            return True
        except OSError as e:
            if config.enableTonsOfPrintInfo == True: print('Access-error on file "' + targetFile + '"! \n' + str(e))
            raise cantAccessException
            return False


def checkDir(file_name):
    '''because who wants to throw an error?  I reused this code like four times so now it's a function.'''
    directory = os.path.dirname(file_name)
    if not os.path.exists(directory):
        os.makedirs(directory)

def checkCSV(fileLocation):
    '''more complicated than checkDir, this will create a CSV file with the header from above if there isn't a file already there.'''
    if os.path.isfile(fileLocation):
        if config.enableTonsOfPrintInfo == True: print("file exists")
        if not canAccess(fileLocation):
            pass
    else:
        if config.enableTonsOfPrintInfo == True: print("file doesn't exist")
        fileDir = os.path.dirname(fileLocation)
        if not os.path.isdir(fileDir):
            os.makedirs(fileDir)
        with open (fileLocation,'a', newline='') as csvfile:
            firstlinewriter = csv.writer(csvfile,delimiter=',')
            firstlinewriter.writerow(csvHeaders)
            csvfile.close()

def appendResultsToCSV(fileLocation,results):
    '''actually writes the CSV data to CSV files.'''
    checkCSV(fileLocation)
    with open (fileLocation,'a', newline='',encoding='utf-8') as csvfile:
            linewriter = csv.writer(csvfile,delimiter=',')
            linewriter.writerow(results)
            csvfile.close()

# Tweaked, enabled not using FTP server:

# Step One: set up connection to FTP server
if config.UseFTP == True: ftpTesting = FTPhandler.ftpHandler(config.FTPcredentials,config.FTP_baseDir,config.FTP_CSVfolder,config.FTP_IMGfolder,config.local_baseDir,config.local_CSVfolder,config.local_IMGfolder,True)
# Step Two: pull results from FTP server so that it has the most recent copy on hand. Not having a file in the server winds up being okay, because appendresultstoCSV will create a CSV if there isn't one available.
if config.UseFTP == True: ftpTesting.getAllCSV()
if config.UseFTP == True: ftpTesting.getCSV(config.outputCSVfile)
# Step Three- get results from speedtest-cli, turn them into CSV format, and then save them to the local CSV copy.
outputLocation = os.path.join(config.local_baseDir,config.local_CSVfolder,config.outputCSVfile)
if config.enableTonsOfPrintInfo == True: print(outputLocation)
if config.enableSpeedtestUpdate == True: print("running speedtest now")
appendResultsToCSV(outputLocation,outputAsList(formatResults(getSpeedtestResults())))
if config.enableSpeedtestUpdate == True: print("speedtest finished")
# Step Four- upload the updated CSV file to the FTP server
if config.UseFTP == True: ftpTesting.uploadCSV(config.outputCSVfile)

# Step Five- download the image from CSV
print("pulling image")
speedtestResultImage = imageHandler.getImage(os.path.join(config.local_baseDir,config.local_CSVfolder,config.outputCSVfile),config.local_baseDir,config.local_IMGfolder,config.enableTonsOfPrintInfo)
print("modifying image")
modifiedImage = imageHandler.modifyImage(config.local_baseDir,config.local_IMGfolder,speedtestResultImage,config.replaceLocation,config.replaceISP,config.replacementForLocation,config.replacementForISP,config.fontURL)
modifiedImage[0].show()
print(modifiedImage[1])
# Step Six: Push image to FTP server
if config.enableTonsOfPrintInfo == True: print("running FTP Test")
print(f"Output File: {speedtestResultImage}")
if config.UseFTP == True: ftpTesting.uploadIMG(modifiedImage[1],speedtestResultImage)

if config.deleteBaseImage == True: os.remove(os.path.join(config.local_baseDir,config.local_IMGfolder,speedtestResultImage))
# if config.enableTonsOfPrintInfo == True: 
print("SUCCESS 💯")

