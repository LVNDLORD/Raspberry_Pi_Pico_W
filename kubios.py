# INFO https://analysis.kubioscloud.com/v2/portal/documentation/api_analytics.html#analyze-a-dataset-v2

import network
import socket
from time import sleep
from machine import I2C, Pin
import ssd1306
import urequests as requests
import ujson


ssid = "<your Wifi name>"
password = "<your Wifi password>"

APIKEY = "<your Kubios API key>"
CLIENT_ID = "<your client ID to Kubios Cloud>"
CLIENT_SECRET = "<your client secret to Kubios Cloud>"
LOGIN_URL = "<your Kubios Cloud Login URL>"
TOKEN_URL = "<your Kubios Cloud authentication Token>"
REDIRECT_URI = "<your Kubios Cloud analysis login link>"


def calculate_data_in_cloud(peak2peak_intervals):
    def connect():
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, password)
        while wlan.isconnected() == False:
            print('Waiting for connection...')
            sleep(1)
        #print(wlan.ifconfig())
        ip = wlan.ifconfig()[0]
        print(f'Connected on {ip}')
        return ip
    
    
    try:
        ip = connect()
    except KeyboardInterrupt:
        machine.reset()
        

    response = requests.post(
        url = TOKEN_URL,
        data = 'grant_type=client_credentials&client_id={}'.format(CLIENT_ID),
        headers = {'Content-Type':'application/x-www-form-urlencoded'},
        auth = (CLIENT_ID, CLIENT_SECRET))

    response = response.json() 
    access_token = response["access_token"] # Parse access token out of the response dictionary
    #crazy
    intervals = peak2peak_intervals
    print(f"Intervals:\n{intervals}")

    data_set = {"type": "RRI", "data": intervals, "analysis" : {"type": "readiness"}}

    response = requests.post(
        url = "https://analysis.kubioscloud.com/v2/analytics/analyze",
        headers = { "Authorization": "Bearer {}".format(access_token),
        "X-Api-Key": APIKEY },
        json = data_set)
    response = response.json()
    #print(response)

    sns = response["analysis"]["sns_index"]
    pns = response["analysis"]["pns_index"]
    sdnn = response["analysis"]["sdnn_ms"]
    mean_bpm = response["analysis"]["mean_hr_bpm"]
    print(mean_bpm)
    print(sns)
    print(pns)
    print(sdnn)

    i2c = I2C(1, sda=Pin(14), scl=Pin(15))
    display = ssd1306.SSD1306_I2C(128, 64, i2c)

    #Print out the SNS and PNS values on the OLED screen
    display.fill(0)
    display.text(f"BPM: {mean_bpm:.2f}", 0, 0)
    display.text(f"SNS Index: {sns:.2f}", 0, 15)
    display.text(f"PNS Index: {pns:.2f}", 0, 30)
    display.text(f"SDNN: {sdnn:.2f}", 0, 45)
    display.show()

