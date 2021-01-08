# python-speedtest-manager
Runs ``speedtest-cli``, pulls from FTP and saves CSV, also modifies result pngs by removing PII (Coming Soon! TM)

The body of this was written in one day on a whim by someone who is *not* a programmer by trade- this works for me, and I've tried to make this work as well as I can for others.

## Dependencies:
### ``speedtest-cli``
``pip install speedtest-cli``
### ``Pillow`` - for working with images.
``pip install pillow``
### ``requests``
``pip install requests``

## Configuration File:
Change this to fit your needs.
As stated, I'd *highly* recommend leaving socket.gethostname() in there in case you have multiple things running this- if you do, then you can just fork this repo, change the config, and push.

```python

FTPcredentials = credentials('server.domain','username','password')

FTP_baseDir = "main/python-speedtest"
FTP_CSVfolder = "csv"
FTP_IMGfolder = "img"


local_baseDir = os.path.realpath('.')
local_CSVfolder = "csv"
local_IMGfolder = "img"


# This can be whatever you want it to be, I'd recommend keeping socket.gethostname() in there somewhere so that if you have multiple instances of this they all have separate places to upload.
outputFile = socket.gethostname()+"-results"+".csv" 

print(os.path.join(local_baseDir,local_CSVfolder,outputFile))

enableTonsOfPrintInfo = False # This is mostly for debugging.
enableSpeedtestUpdate = True  # Mostly for peace of mind.
```