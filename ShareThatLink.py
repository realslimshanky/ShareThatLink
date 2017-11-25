import os
import json

configError = "Please open config.txt file located in the project directory and relace the value '0' of Telegram-Bot-Token with the Token you recieved from botfather"
if 'config.txt' not in os.listdir():
    with open('config.txt', mode='w') as f:
        json.dump({ 'Telegram-Bot-Token': 0 }, f)
        print(configError)
else:
    with open('config.txt', mode='r') as f:
        config = json.loads(f.read())
        if config["Telegram-Bot-Token"]:
            print("Token Present")
        else:
            print(configError)

