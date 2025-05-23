from playwright.sync_api import sync_playwright
import time
import speedtest
import os
from datetime import datetime
import pytz


def test_internet_speed():
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1_000_000
    return download_speed

def restart():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('http://192.168.10.1/cgi-bin/luci')
        page.fill("input[name='luci_password']", "Rakibinto100")
        page.click("button[type='submit']")
        page.wait_for_load_state("networkidle")


        page.goto("http://192.168.10.1/cgi-bin/luci/admin/panel")
    
        page.wait_for_load_state("networkidle")
        page.click('button[onclick*="/cgi-bin/luci/admin/system/reboot/reboot"]')
        

        page.wait_for_selector('button[name="cbi.apply"]')
        page.click('button[name="cbi.apply"]')
        page.wait_for_load_state("networkidle")
        time.sleep(5)


        browser.close()

def saveLog(status):
    bd_tz = pytz.timezone('Asia/Dhaka')
    bd_time = datetime.now(bd_tz)
    standertTimeFormat = bd_time.strftime('%Y-%m-%d %I:%M:%S %p')
    file_path = os.path.dirname(os.path.abspath(__file__))
    file_path= file_path.replace("\\", "/")
    if status == "done":
        message = f"\nRestared at {standertTimeFormat}"
    elif status == "faild":
        message = f"\nFaild at {standertTimeFormat}"
    elif status == "skip":
        message = f"\nSkiped at {standertTimeFormat}"
    else:
        message = f"\nUnknown error at {standertTimeFormat}"
    with open(file_path+"/log.txt", "a") as f:
        f.write(message)




if __name__ == "__main__":
    status= "faild"
    try:
        speed = (test_internet_speed()+test_internet_speed())/2
    except:
        speed =  0
    if speed < 10:
        try:
            restart()
            status =  "done"
        except:
            try:
                restart()
                status = "done"
            except:
                status = "faild"
                pass
    else:
        status = 'skip'
    saveLog(status)