# WeenieBot
Your every day Discord Bot! Included Features: quotes, quote adding/deleting, Cleverbot integration, Admin whitelist for certain Commands, Adding admins by a person's Discord ID, and more!  

# Installing WeenieBot

  First off, run `python3 -m pip install -U -r requirements.txt` to install everything needed for WeenieBot to run. Create an application here: https://discordapp.com/developers/applications/me to make a bot, than make the bot a bot user
by following the steps here: https://discordapp.com/developers/docs/topics/oauth2 make sure you set your application to bot user, that is very important! Don't forget to add WeenieBot to your server by copying your applications ClientID, than going to this link https://discordapp.com/oauth2/authorize?client_id=CLIENT_ID_GOES_HERE&scope=bot&permissions=0 and pasting your Client ID in place of `CLIENT_ID_GOES_HERE`. Make a special Role for your bot, give it ALL permissions, even Administrator.

# Making the Code work for your bot!
Next right-click your discord name and click "Copy ID" than open WeenieBot.py and look for `admin = [""]` paste your ID in between the parenthases, and scroll all the way down until you find `client.run('Your-Bot-Token-Here!')` and replace Your-Bot-Token-Here, with your Application's Token, save and exit WeenieBot.py.

# Thats It!
now just `run python3 WeenieBot.py`
For more info on commands, use the !help command once the bot is up and running!
If you have any questions, or need help. Feel Free to ask!


Made by: Beefywhale @ https://github.com/Beefywhale
Special thanks to: Dragon5232/Armored-Dragon @https://github.com/Armored-Dragon 
