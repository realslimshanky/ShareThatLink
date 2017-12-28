import os
import re
import json
import json
import sys
import signal
import requests
import subprocess


from telegram.ext import Updater, CommandHandler, MessageHandler, filters

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
        json.dump({'Telegram-Bot-Token': 0, 'Telegram-Group-ID': 0, 'Slack-Channel-Webhook': 0}, f)
        print(configError)
        sys.exit(0)
else:
    with open('config.txt', mode='r') as f:
        config = json.loads(f.read())
        if config["Telegram-Bot-Token"] and config["Telegram-Group-ID"] and config["Slack-Channel-Webhook"]:
            print("Token Present, continuing...")
            TelegramBotToken = config["Telegram-Bot-Token"]
            TelegramGroupID = config["Telegram-Group-ID"]
            SlackChannelWebhook = config["Slack-Channel-Webhook"]
        else:
            print(configError)
            sys.exit(0)
"""
---Token/Key Management Ends---
"""

updater = Updater(TelegramBotToken)

def start(bot, update):
    print(update)

def checkForUrl(bot, update):
    User = update.message.from_user
    if str(update.message.chat.id) == TelegramGroupID:
        print(update.message.from_user)
        URLs = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', update.message.text)
        if len(URLs):
            print("/n".join(URLs))
            data = {'text': "{0} shared the following resource(s) on TPB Telegram Group.\n{1}".format(User.first_name+" "+User.last_name, "/n".join(URLs))}
            requests.post(SlackChannelWebhook, data=json.dumps(data), headers={'Content-type': 'application/json'})


updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(MessageHandler(filters.Filters.text, checkForUrl))

updater.start_polling()
