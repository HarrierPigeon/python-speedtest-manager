import os
import socket



class credentials:
    def __init__(self, serverAddress, username,password):
        self.serverAddress = serverAddress
        self.username = username
        self.password = password


UseFTP = True

FTPcredentials = credentials('server.domain','username','password')

FTP_baseDir = "main/python-speedtest"
FTP_CSVfolder = "csv"
FTP_IMGfolder = "img"


local_baseDir = os.path.realpath('.')
local_CSVfolder = "csv"
local_IMGfolder = "img"


# This can be whatever you want it to be, I'd recommend keeping socket.gethostname() in there somewhere so that if you have multiple instances of this they all have separate places to upload.
outputCSVfile = socket.gethostname()+"-results"+".csv" 

print(os.path.join(local_baseDir,local_CSVfolder,outputCSVfile))

enableTonsOfPrintInfo = False # This is mostly for debugging.
enableSpeedtestUpdate = True  # Mostly for peace of mind.

# ImageHandler Stuff

fontURL = "http://db.onlinewebfonts.com/t/056353a27c68233bab7e618c8b191d65.ttf"
replaceISP = True
replacementForISP = "HarrierPigeon, Inc."
replaceLocation = True
replacementForLocation = socket.gethostname()
imagePrepend = "output"
baseImagePrepend = "input"
deleteBaseImage = False