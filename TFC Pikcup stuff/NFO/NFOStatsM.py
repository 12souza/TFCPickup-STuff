import socket
from ftplib import FTP
import os
import zipfile
import discord
from discord.ext import commands
import json

with open('login.json') as f:
    logins = json.load(f)
client = commands.Bot(command_prefix = "!")
'''UDP_IP_ADDRESS = "0.0.0.0"
UDP_PORT_NO = 6789
serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))'''


@client.command(pass_context=True)
@commands.cooldown(1, 300, commands.BucketType.default)
async def stats(ctx, region = None):
    schannel = await client.fetch_channel(1000847501194174675)
    if(region.lower() == "none"):
        await ctx.send("please specify region..")
    elif(region.lower() == 'east' or region.lower() == 'central'):
      try:
        ftp = FTP(logins[region][0])
        ftp.login(user= logins[region][1], passwd=logins[region][2])
        ftp.cwd('tfc')
        ftp.cwd('logs')

        list = ftp.nlst()

        newList = []
        for i in list:
            size = (ftp.size(i))
            if((size > 300000) and (".log" in i)):
                newList.append(i)

        logToParse1 = newList[-2]
        logToParse2 = newList[-1]

        try:
            ftp.retrbinary("RETR " + logToParse1 ,open(logToParse1, 'wb').write)
            ftp.retrbinary("RETR " + logToParse2 ,open(logToParse2, 'wb').write)
        except:
            print("Error")

        f = open(logToParse1)
        pDate = None
        pMap = None
        for line in f:
          if("Loading map" in line):
            mapstart = line.find('map "') + 5
            mapend = line.find('"', mapstart)
            datestart = line.find('L ') + 2
            dateend = line.find('-', datestart)
            pDate =  line[datestart:dateend]
            pMap = line[mapstart:mapend]
        f.close()


        #os.system(f"cp {logToParse1} coachn-{logToParse1}")
        #os.system(f"cp {logToParse2} coachn-{logToParse2}")

        #logToParse1 = "coachn-" + logToParse1
        #logToParse2 = "coachn-" + logToParse2
        #print(logToParse1[7:])
        #print(logToParse2[7:])
        #newCMD = 'curl -v -F "process=true" -F "inptImage=@' + logToParse1 + '" -F "language=en" -F "blarghalyze=Blarghalyze!" http://blarghalyzer.com/Blarghalyzer.php'
        #output = os.popen(newCMD).read()
        #newCMD = 'curl -v -F "process=true" -F "inptImage=@' + logToParse2 + '" -F "language=en" -F "blarghalyze=Blarghalyze!" http://blarghalyzer.com/Blarghalyzer.php'
        #output2 = os.popen(newCMD).read()
        #site = "**Round 1:** https://blarghalyzer.com/parsedlogs/" + logToParse1[:-4].lower() + "/ **Round 2:** https://blarghalyzer.com/parsedlogs/" + logToParse2[:-4].lower() + "/"
        newCMD = 'curl -X POST -F logs[]=@' + logToParse1 + ' -F logs[]=@' + logToParse2 + ' http://app.hampalyzer.com/api/parseGame'
        output3 = os.popen(newCMD).read()
        hampa = "http://app.hampalyzer.com/" + output3[21:-3]
        os.remove(logToParse1)
        os.remove(logToParse2)
        #os.remove(logToParse1[7:])
        #os.remove(logToParse2[7:])

        '''try:
            os.chdir('..')
            os.chdir('demos')
            list = []
            list = sorted(os.listdir())

            newList = []
            for i in list:
                size = (os.path.getsize(i))
                if((size > 10000000) and (".dem" in i)):
                    newList.append(i)

            demoToZip1 = newList[-2]
            demoToZip2 = newList[-1]
            dDate = pDate.replace("/", "")
            try:
                import zlib
                mode= zipfile.ZIP_DEFLATED
            except:
                mode= zipfile.ZIP_STORED
            newfile = pMap + "-" + dDate + ".zip"
            zip= zipfile.ZipFile(newfile, 'w', mode)
            zip.write(demoToZip1)
            zip.write(demoToZip2)
            zip.close()
            #os.remove(demo)

        except:
            newfile = None'''

        await schannel.send(f"**Hampalyzer:** {hampa} {pMap} {pDate} {region}")
        #if(newfile == None):
            #await pChannel.send(content=f"{site} {pMap} {pDate}\n **Hampalyzer:** {hampa}")

        '''delList = ftp.nlst()
        for i in delList:
          if(i not in newList):
            ftp.delete(i)
        ftp.delete(logToParse1)
        ftp.delete(logToParse2)'''
        '''else:
            #await pChannel.send(file = discord.File(newfile), content=f"{site} {pMap} {pDate}\n **Hampalyzer:** {hampa}")
            os.remove(demoToZip1)
            os.remove(demoToZip2)
            os.remove(newfile)'''
      except Exception as e:
        await ctx.channel.send(f"{e}")

client.run("NTY0MjU2NzQxNTIxMzU4ODU4.GmxUGA.uGRNK04LjNJa3kuUli8JSIU5Ax2paUTpdh_LsI")