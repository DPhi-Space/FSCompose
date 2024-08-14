import requests
import threading
import json
import time
import subprocess
from jinja2 import Environment, FileSystemLoader
import json
import os
import subprocess
from otv import *
from requests_toolbelt import MultipartEncoder
from getpass import getpass

CMD_FILE = 'cmds-clients.bin'

def login(username, pwd):
    url = "http://ops.dphi.space:8000/api/login"
    
    data = {"username": username, "password": pwd}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        print("Login successful")
        return response.json()
    else:
        print("Login failed")

def get_zip(token):
    url = "http://ops.dphi.space:8000/api/upload_zip/"
    token_str = f"Token {token}"
    headers = {"Authorization": token_str}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Zip retrieved successfully")
        with open('payloads_files.zip', 'wb') as f:
            f.write(response.content)
        return True
    else:
        print("Failed to retrieve zip")
        return False
        
def send_zip(token):
    url = "http://ops.dphi.space:8000/api/upload_zip/"
    file_path = './downlink.zip'
    if os.path.exists(file_path):
        m = MultipartEncoder(fields={'file': (os.path.basename(file_path), open(file_path, 'rb'))})
        token_str = f"Token {token}"
        headers = {
            "Authorization": token_str,
            "Content-Type": m.content_type
        }
        
        response = requests.post(url, headers=headers, data=m)

        if response.status_code == 200:
            print("Zip sent successfully")
        else:
            print(f"Failed to send zip {response.status_code}")
    else:
        print("The downlink.zip file does not exist")

def setup_fs():
    with open('./deploy/providers.json') as f:
        provider_json = json.load(f)

    env = Environment(loader=FileSystemLoader("deploy/"))
    template = env.get_template('docker-compose-template.txt')

    content = template.render(provider_json['providers'][0])
    with open('docker-compose.yml', mode='w', encoding='utf-8') as f:
        f.write(content)
    try:
        subprocess.run(['docker', 'compose', 'pull'], check=True)
    except:
        
        print("\n[ERROR] Failed to pull containers from the registry.")
        print("⚠️  Have you logged in to the registry?")
        print("\n🔑  Run the following command to log in with your credentials:\n")
        print("   docker login ops.dphi.space")
        print("\n📧  (Credentials were provided via email)\n")

        exit()
    subprocess.run(['docker', 'compose', 'up', '-d'])
    subprocess.run(['docker', 'cp', './deploy/providers.json', 'fsw:/app/providers.json'])
    subprocess.run(['docker', 'cp', './deploy/pdb_fun.stub.py', f"fsw:/app/payloads/{provider_json['providers'][0]['name']}/pdb_fun.py"])

    print("Setup ready!")


if __name__ == "__main__":
    print("Starting FS Interface")
    username = input("Username: ")
    pwd = getpass("Password: ")
    token = login(username, pwd)    
    
    if token:
        get_zip(token['token'])
        print('Starting fs...')
        setup_fs()
        time.sleep(5)
        print('Starting fs-interface...')
        th_interface = threading.Thread(target=fs_interface, args=(CMD_FILE,))
        th_interface.start()
        
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
                    send_zip(token['token'])
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
        
        # stop docker compose 
        subprocess.run(['docker', 'compose', 'down'])
                
        
            
    
    
        