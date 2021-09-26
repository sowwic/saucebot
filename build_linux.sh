 #!/bin/bash  
APP_NAME="saucebot"
MAIN_FILE_PATH=saucebot/bot.py
# Replace python version if not 3.9
SITE_PACKAGES_PATH=.env/lib64/python3.9/site-packages
COGS_DIR="./cogs;./cogs"
ICON_PATH="./res/icon.ico"

python3 -m PyInstaller --onedir --noconsole \
--icon $ICON_PATH \
--paths $SITE_PACKAGES_PATH \
--add-data=$COGS_DIR \
--hidden-import="saucenao_api" \
-n $APP_NAME \
$MAIN_FILE_PATH

# Create empty .env file
ENV_FILE="./dist/saucebot/.env"
touch $ENV_FILE
echo "DISCORD_TOKEN=" >> $ENV_FILE
echo "NAO_KEY=" >> $ENV_FILE

$SHELL 
