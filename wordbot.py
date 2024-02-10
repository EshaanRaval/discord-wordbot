import discord
import random
import requests
import json
from discord.ext import commands
from discord import Interaction
from discord import app_commands

from bs4 import BeautifulSoup
## Day 1 Edit: 
## Imma go sleep now (I started at 8 and now it's 11 and i have math 138 (physics) quiz tomorrow so yeah!)
## Look at the code i wrote so far (i made a lot of progress)


## Day 2 Edit:
## **Tried** learning slash commands and fixing the define categories of commands (still doesn't work)
## Did not make considerable amount of progress but i think i understand how to work with slash commands now 

### Day 3:


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = 'w.', intents=intents)

global desired_channel, game_on, previous_word, used_words

last_letter = ''
desired_channel = None
game_on = False
previous_word = None
respondent_id = ''
used_words = {}

allowed_user = [556413007823896587, 687687366500286649]
prohibited_words= ['anal', 'anus', 'arse','ass','ballsack','balls','bastard','bitch','biatch','bloody','blowjob','blow job','bollock','bollok','boner','boob','bugger','bum','butt','buttplug','clitoris','cock','coon','crap','cunt','damn','dick','dildo','dyke','fag','feck','fellate','fellatio','felching','fuck','fudgepacker','flange','hell','homo','jerk','jizz','knobend','labia','lmao','lmfao','muff','nigger','nigga','omg','penis','piss','poop''prick', 'pube''pussy','queer','scrotum','sex','shit','s hit','sh1t','slut','smegma','spunk', 'tit','tosser','turd', 'twat', 'vagina','wank', 'whore', 'wtf']


@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.activity.CustomActivity(name = "Contemplating the meaning of life, the universe, and whether a synonym for 'serendipity' is just 'happenstancy.'"), status = discord.Status.idle)
    await bot.tree.sync(guild = discord.Object(id = 556414711160242186))
    print(f'Logged in as {bot.user.name}')



@bot.command()
async def start(message):
    global game_on, desired_channel, last_letter
    
    if message.author.id in allowed_user:
        game_on = True
        desired_channel = message.channel
        last_letter = random.choice('abcdefghijklmnopqrstuvwxyz')
        await message.channel.send(f"""Starting the word game in {desired_channel.mention}. 
Let the game begin! The first letter is: **{last_letter.upper()}**""")
    else:
        await message.channel.send('Sorry, Only CU Staff members can use this command to start the game')

@bot.command()
async def end(message):
    global game_on, desired_channel, previous_word, used_words

    desired_channel = None
    game_on = False
    previous_word = None
    used_words = {}
    
    

    await message.channel.send("""ok boss, I hear ya!
                               See ya!""")


# @bot.command()
# async def define(message):
#     word = message.message.content.split()[1]
#     await message.send(f'{word}')
#     api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
#     response = requests.get(api_url)

#     if response.status_code == 200:
#         data = response.json()
#         if data:
#             meanings = data[0].get('meanings', [])
#             if meanings:
#                 response_text = f"Definitions for {word}:\n\n"
#                 for meaning in meanings:
#                     response_text += f"Part of Speech: {meaning['partOfSpeech']}\n"
#                     for definition in meaning['definitions']:
#                         response_text += f"{definition['definition']}\n"
#                     response_text += "\n"
#                 await message.send(response_text)
#             else:
#                 await message.send(f"No definitions found for {word}.")
#         else:
#             await message.send(f"No data found for {word}.")
#     else:
#         await message.send(f"Failed to fetch data. Status code: {response.status_code}")

# @bot.command()
# async def definewithexample(message):
#     word = message.message.content.split()[1]  # Extract the word from the message content
#     api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
#     response = requests.get(api_url)

#     if response.status_code == 200:
#         data = response.json()
#         if data:
#             meanings = data[0].get('meanings', [])
#             if meanings:
#                 response_text = f"Definitions for {word}:\n\n"
#                 for meaning in meanings:
#                     response_text += f"Part of Speech: {meaning['partOfSpeech']}\n"
#                     for definition in meaning['definitions']:
#                         response_text += f"Definition: {definition['definition']}\n"
#                     examples = meaning.get('examples', [])
#                     if examples:
#                         response_text += "\nExamples:\n"
#                         for example in examples:
#                             response_text += f"- {example}\n"
#                     response_text += "\n"
#                 await message.send(response_text)
#             else:
#                 await message.send(f"No definitions found for {word}.")
#         else:
#             await message.send(f"No data found for {word}.")
#     else:
#         await message.send(f"Failed to fetch data. Status code: {response.status_code}")

@bot.command()
async def definewsyns(message):
    word = message.message.content.split()[1]
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if data:
            meanings = data[0].get("meanings",[])
            if meanings:
                response_text = f"Definitions for {word}:\n\n"
                for meaning in meanings:
                    response_text += f"Part of Speech: {meaning['partofSpeech']}\n"
                    for definitions in meaning['definitions']:
                        response_text += f"Definition: {definition['definition']}\n"
                    synonyms = meaning.get('synonyms', [])
                    if synonyms:
                        response_text += "Synonyms: \n"
                        for synonym in synonyms:
                            responnse_text += f"- {synonym}\n"
                    response_text += "\n"
                await message.send(response_text)
            else:
                await message.send(f"No definitions found for {word}.")
        else:
            await message.send(f"No data found for {word}.")
    else:
        await message.send(f"Failed to fetch data. Status code: {response.status_code}")





# @bot.command()
# async def origin(message):
#     word = message.message.content.split()[1]
#     api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
#     response = requests.get(api_url)
    
#     if response.status_code == 200:
#         data = response.json()
        
#         if data:
#             info = data[0]["origin"]
#             response_text = f"Origin of {word}:\n\n{info}"
#             await message.send(response_text)
#         else:
#             await message.send(f"No data found for {word}.")
#     else:
#         await message.send(f"Failed to fetch data. Status code: {response.status_code}")





###### BOT COMMANDS ############
### info
## Command
@bot.hybrid_command(with_app_command= True)
@app_commands.guilds(discord.Object(id = 556414711160242186))
async def info(message):  
    """Learn Basic Information about the Wordbot to get things rollings"""
    await message.send("I am WordBot, a bot that allows Discord members to play a chat-based word game! Type `w.start` to begin the game.")



### help  (Need to learn how to edit help function)
    
# @bot.command()
# async def help(message):
#     response = "This is a help function (which is appparently still a WIP)"
#     await message.send(response)

@bot.tree.command(name= 'help', description = "lists out all of the commands and what they do (still a WIP)", guild = discord.Object(id= 556414711160242186))
async def shelp(interaction: Interaction):
    await interaction.response.send_message("This is a help function (which is appparently still a WIP)")

### thanks
msg_thanks = "Thanks to..... :"
@bot.hybrid_command(with_app_command=True)
@app_commands.guilds(discord.Object(id = 556414711160242186))
async def thanks(message):
    """Displays a Thank you Message"""
    await message.send(msg_thanks)

### fun fact
fun_fact = {1: "", 2: "", 3: "", 4: "", 5: "",6: "", 7: "", 8: "", 9: "", 10: ""}
@bot.hybrid_command(with_app_command=True)
@app_commands.guilds(discord.Object(id = 556414711160242186))
async def funfact(message):
    index = random.choice(range(len(fun_fact)))
    await message.send(fun_fact[index])



############ story #################################

Story = ""
@bot.hybrid_command(with_app_command=True)
@app_commands.guilds(discord.Object(id = 556414711160242186))
async def lore(message):
    await message.send(Story)

                
############ BOT FUNCTIONALITY ###########

### Define
@bot.hybrid_group(name = "define", with_app_command=True)
@app_commands.guilds(discord.Object(id = 556414711160242186))
async def define(message, word, word_class: str = None):
    await message.send(f'{word}')

@define.command()
@app_commands.guilds(discord.Object(id = 556414711160242186))
async def this(message, word, word_class: str=None):
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        if data:
            meanings = data[0].get('meanings', [])
            if meanings:
                response_text = f"Definitions for {word}:\n\n"
                for meaning in meanings:
                    response_text += f"Part of Speech: {meaning['partOfSpeech']}\n"
                    for definition in meaning['definitions']:
                        response_text += f"{definition['definition']}\n"
                    response_text += "\n"
                await message.send(response_text)
            else:
                await message.send(f"No definitions found for {word}.")
        else:
            await message.send(f"No data found for {word}.")
    else:
        await message.send(f"Failed to fetch data. Status code: {response.status_code}")
    
@define.command()
@app_commands.guilds(discord.Object(id = 556414711160242186))
async def this_with_example(message, word, word_class: str=None):
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if data:
            meanings = data[0].get('meanings', [])
            if meanings:
                response_text = f"Definitions for {word}:\n\n"
                for meaning in meanings:
                    response_text += f"Part of Speech: {meaning['partOfSpeech']}\n"
                    for definition in meaning['definitions']:
                        response_text += f"Definition: {definition['definition']}\n"
                        if 'example' in definition:  # Check if 'example' key exists
                            response_text += f"Example: {definition['example']}\n"
                    response_text += "\n"
                await message.send(response_text)
            else:
                await message.send(f"No definitions found for {word}.")
        else:
            await message.send(f"No data found for {word}.")
    else:
        await message.send(f"Failed to fetch data. Status code: {response.status_code}")


## Command
## Slash                
## #Define with examples
## Command
## Slash
### Origin/Epytomology
## Command

@bot.hybrid_command(with_app_command=True)
@app_commands.guilds(discord.Object(id = 556414711160242186))
async def origin(message, word):
    """get_etymology"""
    url = f"https://www.etymonline.com/word/{word}"
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response2 = requests.get(api_url)
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        reply = soup.find("section", class_="word__defination--2q7ZH").get_text().strip()
        # print("This is the printed ans"+ans)
        
    elif response2.status.code != 200:
        reply = "Sorry, we couldn't find that word"
    else: 
        reply = "Sorry, We Couldn't find the origin of this word"
    await message.send(reply)
## Slash
 
### Quote --> https://api.quotable.io/
# Genre Based:
# random:
@bot.command()
async def quote(message):

    url = "https://api.quotable.io/quotes/random"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # print(data[0])
        # print(data[0]['content'])
        reply = f" \"{data[0]['content']}\" - {data[0]['author']}"
    else:
        reply = f"Sorry something went wrong: [Error: {response.status.code}]"
    await message.send(reply)
      
                
### Word Games --> https://dictionaryapi.dev
# Word Chain

# Command to play the game
        
@bot.event
async def on_message(message):
    global last_letter, game_on, desired_channel, previous_word, respondent_id
    command = message.content.split()[0]
    args = message.content.split()[1:0]

    
    if message.author == bot.user:
        return 
    
    ## Check if the message is a command
    await bot.process_commands(message)

    ## Game Code

    if game_on:
        if message.content == 'w.end':
            return
        if message.channel != desired_channel:
            return

        if message.author == bot.user or message.content.startswith(('!', '.', '>')):
            return
        
        if message.author.id == respondent_id:
            await message.delete()
            await message.channel.send('You cant send all the words, let other members join in on the fun as well')

        if message.channel == desired_channel and message.author != bot.user and not message.content.lower().startswith(last_letter):
            await message.delete()
            await message.channel.send(f' {message.author.mention}Invalid word. Please start your word with the letter **{last_letter.upper()}**.')

        if message.channel == desired_channel and message.content.lower().startswith(last_letter) and len(message.content) > 1 and message.author.id != respondent_id:
            word = message.content.lower()
            # Check if the word is in the Oxford dictionary (simplified check)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response_word = requests.get(f'https://www.oxfordlearnersdictionaries.com/definition/english/{word}', headers=headers)
            
            if response_word.status_code == 200:
                await message.add_reaction('<:CU_Accept:866720792578359317>')  # React with a checkmark emoji
                last_letter = word[-1]  # Update the last letter
                previous_word = word
                respondent_id = message.author.id
            else:
                await message.channel.send("Sorry, that word is not in the dictionary. Try another word.")


# One Word Story


# Hangman (possible?)



######






bot.run('OTMzMjU1ODIwMjQ0ODM2NDAy.GGmAQX.HfdYfyveybqJoctvp4Dm9cCnxMD0aBlFQeyBpU')
