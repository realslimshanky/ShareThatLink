import os
import json
import json
import sys
import signal
import subprocess

"""
---Process ID Management Starts---
This part of the code helps out when you want to run your program in background using '&'. This will save the process id of the program going in background in a file named 'pid'. Now, when you run you program again, the last one will be terminated with the help of pid. If in case the no process exist with given process id, simply the `pid` file will be deleted and a new one with current pid will be created.
"""
currentPID = os.getpid()
if 'pid' not in os.listdir():
    with open('pid', mode='w') as f:
        print(str(currentPID), file=f)
else:
    with open('pid', mode='r') as f:
        try:
            os.kill(int(f.read()), signal.SIGTERM)
            print("Terminating previous instance of " +
                  os.path.realpath(__file__))
        except ProcessLookupError:
            subprocess.run(['rm', 'pid'])
    with open('pid', mode='w') as f:
        print(str(currentPID), file=f)
"""
---Process ID Management Ends---
"""

"""
---Token/Key Management Starts---
This part will check for the config.txt file which holds the Telegram and will also give a user friendly message if they are invalid. New file is created if not present in the project directory.
"""
configError = "Please open config.txt file located in the project directory and relace the value '0' of Telegram-Bot-Token with the Token you recieved from botfather."
if 'config.txt' not in os.listdir():
    with open('config.txt', mode='w') as f:
        json.dump({'Telegram-Bot-Token': 0}, f)
        print(configError)
        sys.exit(0)
else:
    with open('config.txt', mode='r') as f:
        config = json.loads(f.read())
        if config["Telegram-Bot-Token"]:
            print("Token Present, continuing...")
            TelegramBotToken = config["Telegram-Bot-Token"]
        else:
            print(configError)
            sys.exit(0)
"""
---Token/Key Management Ends---
"""

