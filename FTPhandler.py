import ftplib
import os
import config

# Special thanks to https://www.thepythoncode.com/article/download-and-upload-files-in-ftp-server-using-python for the help :)



class ftpHandler:
    # needs to have:
    # - initialization stuff- can pass a secret class to it for server login data
    # - FTP target directory (may have to spec 2 or subdirs when we pull photos from speedtest.net)
    # - working / temp local directory
    # - Method for getting list of all files in $$ftpFolder
    # - Method for pulling $file and storing in $location
    # - Method for putting $file in $location

    # WILL DO LATER: Basically copy the upload and download things but slightly tweaked for images.  Or maybe a rebase so that I don't have to duplicate code.  IDK.
    def __init__(self,credentials: config.credentials,ftpTargetDir: str,ftpCSVsubDir: str,ftpImageSubDir:str,localWorkingDirectory: str,localCSVDir:str,localImageDir:str,printAbunchOfDebugStatements=False):
        self.creds = credentials
        self.ftpDir = ftpTargetDir
        self.localWorkDir = localWorkingDirectory
        self.ftpCSVsub = ftpCSVsubDir
        self.ftpimgSub = ftpImageSubDir
        self.localCSVsub = localCSVDir
        self.localimgSub = localImageDir
        self.doDebug = printAbunchOfDebugStatements
        
    

    def getAllCSV(self):
        ftpConnection = ftplib.FTP(host=self.creds.serverAddress,user=self.creds.username,passwd=self.creds.password)
        ftpConnection.cwd(self.ftpDir)
        # filetype = '*.csv'
        if not os.path.isdir(self.localWorkDir):
            os.mkdir(self.localWorkDir)
        os.chdir(self.localWorkDir)
        if self.doDebug == True: print(os.getcwd())

        if os.path.isdir(self.localCSVsub):
            pass
        else:
            os.mkdir(self.localCSVsub)
        os.chdir(self.localCSVsub)

        # currently working on making this part more robust.
        if self.doDebug == True: print("testing MLST command\n",ftpConnection.sendcmd('MLST /'))
        if self.doDebug == True: print(ftpConnection.nlst())
        if self.ftpCSVsub in ftpConnection.nlst():
            if self.doDebug == True: print("folder exists")
        #    pass
        else:
            if self.doDebug == True: print("CSV output folder doesn't exist, creating")
            ftpConnection.mkd(self.ftpCSVsub)
            
        checkIsDirString = ftpConnection.sendcmd(f'MLST {self.ftpCSVsub}')
        if "type=dir" in checkIsDirString:
            if self.doDebug == True: print("THAT's A DIRECTORY")
        else:
            if self.doDebug == True: print("THAT'S NOT A DIRECTORY, FIXING")
            ftpConnection.mkd(self.ftpCSVsub)
        ftpConnection.cwd(self.ftpCSVsub)

        if self.doDebug == True: print(os.getcwd())
        if self.doDebug == True: print("ftpConnection.dir()\n",ftpConnection.dir())


        files = ftpConnection.nlst()
        if self.doDebug == True: print(files)
        for filez in files:
            with open(filez, "wb") as file:
                if self.doDebug == True: print(f"retrieving {filez}")
                ftpConnection.retrbinary(f"RETR {filez}", file.write)
        ftpConnection.quit()
        os.chdir(self.localWorkDir)


    def uploadCSV(self,fileLocation:str):
        if self.doDebug == True: print("uploadCSV called")
        ftpConnection = ftplib.FTP(host=self.creds.serverAddress,user=self.creds.username,passwd=self.creds.password)
        ftpConnection.cwd(self.ftpDir)

        ftpConnection.cwd(self.ftpCSVsub)

        if self.doDebug == True: print(os.getcwd())

        if not os.path.isdir(self.localWorkDir):
            os.mkdir(self.localWorkDir)
        os.chdir(self.localWorkDir)
        if self.doDebug == True: print(os.getcwd())

        if not os.path.isdir(self.localCSVsub):
            os.mkdir(self.localCSVsub)
        os.chdir(self.localCSVsub)


        if self.doDebug == True: print("uploadCSV RAN")
        ftpConnection.sendcmd('MLST /')
        if self.doDebug == True: print(ftpConnection.nlst())

        with open(fileLocation, "rb") as file:
                # use FTP's STOR command to upload the file
            ftpConnection.storbinary(f"STOR {fileLocation}", file)
        
        ftpConnection.quit()


    def getCSV(self,fileName:str):

        ftpConnection = ftplib.FTP(host=self.creds.serverAddress,user=self.creds.username,passwd=self.creds.password)
        ftpConnection.cwd(self.ftpDir)


        if self.ftpCSVsub in ftpConnection.nlst():
            if self.doDebug == True: print("folder exists")
        #    pass
        else:
            if self.doDebug == True: print("CSV output folder doesn't exist, creating")
            ftpConnection.mkd(self.ftpCSVsub)
            
        checkIsDirString = ftpConnection.sendcmd(f'MLST {self.ftpCSVsub}')
        if "type=dir" in checkIsDirString:
            if self.doDebug == True: print("THAT's A DIRECTORY")
        else:
            if self.doDebug == True: print("THAT'S NOT A DIRECTORY, FIXING")
            ftpConnection.mkd(self.ftpCSVsub)
        ftpConnection.cwd(self.ftpCSVsub)

        if not os.path.exists(self.localWorkDir):
            os.mkdir(self.localWorkDir)
        os.chdir(self.localWorkDir)
        if self.doDebug == True: print(os.getcwd())

        if os.path.isdir(self.localCSVsub): 

            os.chdir(self.localCSVsub)
        else:
            os.mkdir(self.localCSVsub)
            os.chdir(self.localCSVsub)

        files = ftpConnection.nlst()
        if fileName in files:
            with open(fileName, "wb") as file:
                # use FTP's RETR command to download the file   
                ftpConnection.retrbinary(f"RETR {fileName}", file.write)

        
        ftpConnection.quit()

    def uploadIMG(self,fileLocation:str,fileName:str):
        if self.doDebug == True: print("uploadIMG called")
        ftpConnection = ftplib.FTP(host=self.creds.serverAddress,user=self.creds.username,passwd=self.creds.password)
        ftpConnection.cwd(self.ftpDir)

        ftpConnection.cwd(self.ftpimgSub)

        if self.doDebug == True: print(os.getcwd())

        if not os.path.isdir(self.localWorkDir):
            os.mkdir(self.localWorkDir)
        os.chdir(self.localWorkDir)
        if self.doDebug == True: print(os.getcwd())

        if not os.path.isdir(self.localimgSub):
            os.mkdir(self.localimgSub)
        os.chdir(self.localimgSub)

        if self.doDebug == True: print("uploadIMG RAN")
        ftpConnection.sendcmd('MLST /')
        if self.doDebug == True: print(ftpConnection.nlst())

        with open(fileLocation, "rb") as file:
            ftpConnection.storbinary(f"STOR {fileName}", file)


        ftpConnection.quit()




