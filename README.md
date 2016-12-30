# WeenieBot
![alt tag](https://discordapp.com/api/guilds/232186009998196739/widget.png?)
Your every day Discord Bot! Included Features: quotes, quote adding/deleting, Cleverbot integration, Admin whitelist for certain Commands, Adding admins by a person's Discord ID, and more!  

# Installing WeenieBot
# Easy Install:
click this link http://tiny.cc/weeniebot to add WeenieBot to a server instantly! Can't promise 100% reliability and uptime!
if you want to install the bot yourself and run it on your own computer look for Harder Install section!

# Harder Install:
  First off, run `python -m pip install -U -r requirements.txt` to install everything needed for WeenieBot to run. Create an application here: https://discordapp.com/developers/applications/me to make a bot, than make the bot a bot user
by following the steps here: https://discordapp.com/developers/docs/topics/oauth2 make sure you set your application to bot user, that is very important! Don't forget to add WeenieBot to your server by copying your applications ClientID, than going to this link https://discordapp.com/oauth2/authorize?client_id=CLIENT_ID_GOES_HERE&scope=bot&permissions=0 and pasting your Client ID in place of `CLIENT_ID_GOES_HERE`. Make a special Role for your bot, give it ALL permissions, even Administrator.

# Making the Code work for your bot!
Next copy your discord name **important** your username not nickname! than open adminweenie.json(with your text editor of choice) and look for `[""]` paste your name in between the parenthases, now open prefix.json, paste your name in the quotes at Your-Discord-Name-Here `"bot_owner": "Your-Discord-Name-Here"`, then open botToken.py(found in modules folder!), scroll all the way down until you find `token = 'Your-Bot-Token-Here!'` and replace Your-Bot-Token-Here, with your Application's Token, save and exit WeenieBot.py.

For a more in-depth guide on Installing and seting up WeenieBot, go here: https://github.com/Beefywhale/WeenieBot/wiki/WeenieBot's-In-depth-setup

# Thats It!
now just `run python WeenieBot.py`
For more info on commands, use the !help command once the bot is up and running!
If you have any questions, or need help. Feel Free to ask!


Made by: Beefywhale @ https://github.com/Beefywhale
Special thanks to: Dragon5232/Armored-Dragon @https://github.com/Armored-Dragon 
