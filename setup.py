'''WeenieBot's Setup!'''
import json
import subprocess
import time
import sys

with open("settings.json", 'w+') as outfile:
	outfile.write(json.dumps({}))
with open("settings.json", "r") as infile:
    settings = json.loads(infile.read())

print('Welcome to WeenieBot\'s setup!\nIf you need any help just refer to the in-depth setup guide at:\nhttps://github.com/Beefywhale/WeenieBot/wiki/WeenieBot\'s-In-depth-setup\n')

install_depend = input('Install Python dependencies? [Y/N]')

if install_depend.lower() in ['yes', 'y']:
	sys.stdout.write('Installing Python packages')
	sys.stdout.flush()
	time.sleep(0.5)
	sys.stdout.write('.')
	sys.stdout.flush()
	time.sleep(0.5)
	sys.stdout.write('.')
	sys.stdout.flush()
	time.sleep(0.5)
	sys.stdout.write('.')
	sys.stdout.flush()
	time.sleep(0.2)
	subprocess.run("python -m pip install -U -r requirements.txt", shell=True, check=True)
else:
	print('Not installing dependencies!')

token = input('\nBot\'s Token: ')
settings['token'] = str(token)
with open("settings.json", 'w+') as outfile:
	outfile.write(json.dumps(settings))

client_id = input('\nClient ID: ')
print('Visit this link to add the bot to your server!\nhttps://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=0'.format(client_id))

print('\n\nThats all! bot setup is complete!')