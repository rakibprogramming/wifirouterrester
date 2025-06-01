import requests
import time
def speedtest():
    startTime = time.time()
    file = requests.get("https://link.testfile.org/AY6sjl",allow_redirects=True)
    endTime = time.time()
    size = (len(file.content)/1024)/1024
    speed = (size/(endTime-startTime))*8
    print(speed)

speedtest()