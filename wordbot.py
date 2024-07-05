import discord
import random
import requests
from discord.ext import commands

# This is just the Original Code

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = 'w.', intents=intents)

last_letter = ''
desired_channel = None
game_on = False
previous_word = None
respondent_id = ''
used_words = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


# Command to play the game
@bot.event
async def on_message(message):
    global last_letter, game_on, desired_channel, previous_word, respondent_id
    command = message.content.split()[0]
    args = message.content.split()[1:0]

    if message.author == bot.user:
        return 
     
    # Command to start the game
    if command == 'w.start':
        allowed_user = [556413007823896587, 687687366500286649]
        if message.author.id in allowed_user:
            game_on = True
            desired_channel = message.channel
            last_letter = random.choice('abcdefghijklmnopqrstuvwxyz')
            await message.channel.send(f"""Starting the word game in {desired_channel.mention}. 
Let the game begin! The game has started! The first letter is: **{last_letter.upper()}**""")
            
        else:
            await message.channel.send('Only allowed members can use this command to start the game')
                    
    # Command to get info about the bot

    if command == 'w.info':
        await message.channel.send("I am WordBot, a bot that allows discord members to play chat based wordgame! Type `w.start` to begin the game.")

    # Wordbot game code
    
    if game_on:
        if message.channel != desired_channel:
            return

        if message.author == bot.user or message.content.startswith(('!', '.', '>')):
            return
        
        if message.author.id == respondent_id:
            await message.delete()
            await message.channel.send('You cant send all the words, let other members join in on the fun as well')

        if message.channel == desired_channel and message.content != 'w.start' and message.author != bot.user and not message.content.lower().startswith(last_letter):
            await message.delete()
            await message.channel.send(f' {message.author.mention}Invalid word. Please start your word with the letter **{last_letter.upper()}**.')

        if message.channel == desired_channel and message.content.lower().startswith(last_letter) and len(message.content) > 1 and message.author.id != respondent_id:
            word = message.content.lower()
            # Check if the word is in the Oxford dictionary (simplified check)   header is a user-agent header for http request ("the User-Agent header is an HTTP header intended to identify the user agent responsible for making a given HTTP request")  understood from: https://www.geeksforgeeks.org/http-headers-user-agent/
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response_word = requests.get(f'https://www.oxfordlearnersdictionaries.com/definition/english/{word}', headers=headers)
            
            if response_word.status_code == 200:
                await message.add_reaction('<:CU_Accept:866720792578359317>')  # React with a checkmark emoji
                last_letter = word[-1]  # Update the last letter
                previous_word = word
                respondent_id = message.author.id
            else:
                await message.channel.send("Sorry, that word is not in the dictionary. Try another word.")






bot.run('OTMzMjU1ODIwMjQ0ODM2NDAy.GGmAQX.HfdYfyveybqJoctvp4Dm9cCnxMD0aBlFQeyBpU')
