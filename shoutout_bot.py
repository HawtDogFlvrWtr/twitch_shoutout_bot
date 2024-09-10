import configparser
import twitchio
from twitchio.ext import commands, routines
from tkinter import Tk, Label, Entry, Button, StringVar, Frame
import customtkinter
from datetime import date, datetime
from tinydb import TinyDB, Query
import time

# Create and initialize the configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Database Setup
database = TinyDB('shoutout_users.json', indent=4)
db = Query()

# Variables
shoutout_wait_queue = []
last_shoutout = 0
is_live = False

# Create initial bot configuration GUI
class BotConfigGUI:
    def __init__(self, master, config):
        self.master = master
        self.master.title("Auto Shoutout Bot")

        # Create labels and entry fields for each configuration option
        self.entries = {}
        row_number = 0
        for option, value in config['ShoutoutBot'].items():
            customtkinter.CTkLabel(self.master, text=option.replace('_', ' ').title()).grid(row=row_number, column=0, padx=10, pady=5)
            self.entries[option] = customtkinter.CTkEntry(self.master)
            self.entries[option].insert(0, value)
            self.entries[option].grid(row=row_number, column=1, padx=10, pady=5)
            row_number += 1

        # Create a button to update the configuration
        customtkinter.CTkButton(self.master, text="Update Configuration", command=self.update_config).grid(row=row_number, columnspan=2, pady=10)

    def update_config(self):
        # Get values from entry fields and update the configuration
        for option, entry in self.entries.items():
            config['ShoutoutBot'][option] = entry.get()
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        self.master.destroy()

# Initialize and display the bot configuration GUI
root = customtkinter.CTk()
frame = customtkinter.CTkFrame(master=root, width=200, height=200)
bot_config_gui = BotConfigGUI(root, config)
root.mainloop()

shoutout_cooldown_seconds = int(config['ShoutoutBot']['shoutout_cooldown_hours']) * 60 * 60
shoutout_wait_seconds = int(config['ShoutoutBot']['shoutout_wait_seconds'])

class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=config['ShoutoutBot']['twitch_token'], prefix=config['ShoutoutBot']['bot_prefix'], initial_channels=[config['ShoutoutBot']['channel']])

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as: {self.nick}')
        print(f'User id is: {self.user_id}')

    async def event_message(self, message):
        global shoutout_wait_queue
        global is_live
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return
        
        author = f'@{message.author.name}'
        find_user = database.search(db.username == author)
        if len(find_user) > 0 and is_live: # Is it in our DB?
            current_epoch = time.time()
            last_shoutout = float(find_user[0]['last_shoutout'])
            # Check if we've met our cooldown if its someone we track
            if current_epoch - last_shoutout >= shoutout_cooldown_seconds:
                if author not in shoutout_wait_queue:
                    shoutout_wait_queue.append(author)
                    database.update({'last_shoutout': current_epoch}, db.username == author)
        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    @commands.command()
    async def addso(self, ctx: commands.Context):
        global shoutout_wait_queue
        short_date = date.today().strftime("%a %b %d %Y")
        split_chat = ctx.message.content.split()
        current_epoch = time.time()
        if len(split_chat) > 1: # Do we have a username?
            username = split_chat[1].lower()
            find_user = database.search(db.username == username)
            if len(find_user) > 0: # Is it in our DB?
                await ctx.send(f'{username} exists.')
                if username not in shoutout_wait_queue:
                    shoutout_wait_queue.append(username)
                database.update({'last_shoutout': current_epoch}, db.username == username)
            else:
                database.insert({'username': username, 'added_date': short_date, 'last_shoutout': current_epoch})
                await ctx.send(f'{username} added.')
                if username not in shoutout_wait_queue:
                    shoutout_wait_queue.append(username)

    @commands.command()
    async def removeso(self, ctx: commands.Context):
        split_chat = ctx.message.content.split()
        username = split_chat[1]
        find_user = database.search(db.username == username)
        if len(find_user) > 0: # Is it in our DB
            if database.remove(db.username == username):
                await ctx.send(f'{username} removed.')

# Check if live every 5 seconds
@routines.routine(seconds=5.0, iterations=None)
async def check_live():
    global is_live
    fetch_stream = await bot.fetch_streams(user_logins=[config['ShoutoutBot']['channel']])
    if len(fetch_stream) > 0: # Stream is live
        if is_live == False:
            print("Stream has started. Enabling shoutouts.")
        is_live = True
    else:
        if is_live == True:
            print("Stream has ended. Disabling shoutouts.")
        is_live = False

# Check if we should shoutout every 5 seconds
@routines.routine(seconds=2.0, iterations=None)
async def shoutout():
    global is_live
    global shoutout_wait_queue
    global last_shoutout
    global shoutout_wait_seconds
    if is_live and len(shoutout_wait_queue) > 0:
        if last_shoutout + shoutout_wait_seconds < time.time(): # Wait the sleep time between shouting out so the progress bar finishes
            await bot.connected_channels[0].send(f'!so {shoutout_wait_queue.pop(0)}')
            last_shoutout = time.time()
        else:
            remaining_time = time.time() - last_shoutout + shoutout_wait_seconds
            print(f"Waiting {remaining_time}")

bot = Bot()
check_live.start()
shoutout.start()
bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.