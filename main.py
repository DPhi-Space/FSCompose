import requests
import threading
import json
import os
import subprocess
from otv import *
from requests_toolbelt import MultipartEncoder
from getpass import getpass

CMD_FILE = 'cmds-clients.bin'

def login(username, pwd):
    url = "http://127.0.0.1:8000/api/login"
    data = {"username": username, "password": pwd}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        print("Login successful")
        return response.json()
    else:
        print("Login failed")

def get_zip(token):
    url = "http://127.0.0.1:8000/api/upload_zip/"
    token_str = f"Token {token}"
    headers = {"Authorization": token_str}
    print(headers)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Zip retrieved successfully")
        with open('payloads_files.zip', 'wb') as f:
            f.write(response.content)
        return True
    else:
        print("Failed to retrieve zip")
        return False
        
def send_zip():
    url = "http://127.0.0.1:8000/api/upload_zip/"
    #file_path = '/home/jsilveira/DPhi/GS/django_project/downlink.zip'
    file_path = './downlink.zip'
    if os.path.exists(file_path):
        m = MultipartEncoder(fields={'file': (os.path.basename(file_path), open(file_path, 'rb'))})
        headers = {
            "Authorization": "Token 28db0f69442675fc29fea3fcb3b7d44d861d30c7",
            "Content-Type": m.content_type
        }
        
        response = requests.post(url, headers=headers, data=m)

        if response.status_code == 200:
            print("Zip sent successfully")
        else:
            print("Failed to send zip")
    else:
        print("The downlink.zip file does not exist")

if __name__ == "__main__":
    print("Starting FS Interface")
    username = input("Username: ")
    pwd = getpass("Password: ")
    token = login(username, pwd)    
    
    if token:
        #get_zip(token['token'])
        print('Starting fs-interface...')
        th_interface = threading.Thread(target=fs_interface, args=(CMD_FILE,))
        th_interface.start()
        time.sleep(2)
        
        if th_interface.is_alive():
            print('\nPress e to execute Command Sequence')
            print('Press s to send downlink.zip to GS')
            print('Press q to quit\n')
        
        while th_interface.is_alive():
            
            if get_current_state() == STATES['IDLE']:
                key = input(f'Waiting for Instructions ')
                if key.lower() == 'e':
                    if get_zip(token['token']):
                        set_current_state(STATES['EXECUTING_CMDS'])
                    
                elif key.lower() == 's':
                    print('Sending zip to GS...')  
                    send_zip()
                elif key.lower() == 'q':
                    print('Stopping FS Interface...')  
                    set_current_state(STATES['EXIT'])
                    time.sleep(3)
                    th_interface.join()
                    break

            elif get_current_state() == STATES['EXECUTING_CMDS']:
                print('FS executing command sequence...Patience.')
                time.sleep(3)
            elif get_current_state() == STATES['WAITING_DOWNLINK']:
                print('Waiting for downlink files...')
                time.sleep(3)
            
            time.sleep(0.1)  # Small sleep to reduce CPU usage
                
        
            
    
    
        