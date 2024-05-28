import discord
import random as chaos
import requests
import json
from discord.ext import commands
from discord import Interaction
from discord import app_commands
import asyncio
from bs4 import BeautifulSoup
import datetime
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

global desired_channel, word_game_on, previous_word, used_words
### Word Game Variables

last_letter = ''
desired_channel = None
word_game_on = False
previous_word = None
word_respondent_id = ''
used_words = {}

### Count Game Variables
global count_on, count_channel, count_number, count_respondent_id
count_on = False
count_channel = None
count_number = 0
count_respondent_id = ""
### One Word Story Variables
story_on = False
story_channel = None
one_story = []
story_respondent_id = ""
### 

allowed_user = [556413007823896587, 687687366500286649, 1164014463511433316]
prohibited_words= ['anal', 'anus', 'arse','ass','ballsack','balls','bastard','bitch','biatch','bloody','blowjob','blow job','bollock','bollok','boner','boob','bugger','bum','butt','buttplug','clitoris','cock','coon','crap','cunt','damn','dick','dildo','dyke','fag','feck','fellate','fellatio','felching','fuck','fudgepacker','flange','hell','homo','jerk','jizz','knobend','labia','lmao','lmfao','muff','nigger','nigga','omg','penis','piss','poop''prick', 'pube''pussy','queer','scrotum','sex','shit','s hit','sh1t','slut','smegma','spunk', 'tit','tosser','turd', 'twat', 'vagina','wank', 'whore', 'wtf']


@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.activity.CustomActivity(name = "Contemplating the meaning of life, the universe, and whether a synonym for 'serendipity' is just 'happenstancy.'"), status = discord.Status.idle)
    await bot.tree.sync(guild = discord.Object(id = 773492566208675851))
    print(f'Logged in as {bot.user.name}')





## -------------------------------------------------------------------------------------------------------------------------------------- ##

#    /------------------------------------------- B A S I C  | C O M M A N D S ------------------------------------------------------\

##  ------------------------------------------------------ I N F O  ---------------------------------------------------------------------- ##
@bot.hybrid_command(with_app_command= True, aliases = ["test"])
@app_commands.guilds(discord.Object(id = 773492566208675851))
async def info(message):  
    """Learn Basic Information about the Wordbot to get things rollings"""
    await message.send("I am WordBot, a bot that allows Discord members to play a chat-based word game! Type `w.start` to begin the game.")


##  ------------------------------------------------------- H E L P  ---------------------------------------------------------------------- ##
### help  (Need to learn how to edit help function)
    
# @bot.command()
# async def help(message):
#     response = "This is a help function (which is appparently still a WIP)"
#     await message.send(response)

@bot.hybrid_command(with_app_command = True, aliases = ["welp"])
@app_commands.guilds(discord.Object(id = 773492566208675851))
async def shelp(message):
    """Display a list of commands and their respective functionalities (work in progress)."""
    await message.send("This is a help function (which is appparently still a WIP)")


##  ------------------------------------------------------ T H A N K S  ---------------------------------------------------------------------- ##

msg_thanks = "Thanks to..... :"
@bot.hybrid_command(with_app_command=True, aliases = ["thnks", "tk"])
@app_commands.guilds(discord.Object(id = 773492566208675851))
async def thanks(message):
    """Displays a Thank you Message"""
    await message.send(msg_thanks)

##  ------------------------------------------------------ F U N | F A C T  ------------------------------------------------------------------- ##
    
fun_fact = {1: "", 2: "", 3: "", 4: "", 5: "",6: "", 7: "", 8: "", 9: "", 10: ""}
@bot.hybrid_command(with_app_command=True, aliases = ["ffs", "fact", "fun"])
@app_commands.guilds(discord.Object(id = 773492566208675851))
async def funfact(message):
    index = random.choice(range(len(fun_fact)))
    await message.send(fun_fact[index])



##  ------------------------------------------------------- S T O R Y ------------------------------------------------------------------- ##

Story = ""
@bot.hybrid_command(with_app_command=True, aliases = ["Lore","story", "Story"])
@app_commands.guilds(discord.Object(id = 773492566208675851))
async def lore(message):
    await message.send(Story)


## \--------------------------------------------------------------------------------------------------------------------------------------/ ##


#    /------------------------------------------- D E F I N E  | C O M M A N D S ------------------------------------------------------\


##  ------------------------------------------------------- G R O U P ------------------------------------------------------------------- ##
    
@bot.hybrid_group(name = "define", with_app_command=True, aliases = ["Define"])
@app_commands.guilds(discord.Object(id = 773492566208675851))
async def define(message, word, word_class: str = None):
    await message.send(f'{word}')

##  ------------------------------------------------------- D E F I N E ------------------------------------------------------------------- ##

@define.command(name = "this", aliases = ["dis", "This"])
@app_commands.guilds(discord.Object(id = 773492566208675851))
@commands.cooldown(1, 60, commands.BucketType.user)
async def this(message, word, word_class: str=None):
    """Sends all the definition of the specificed word - "word", 
    Note: if you require a definition for a specific word_class (noun, interjection, etc.) you can use the parameter "Word_Class" 
    Note: for word_class spell the entire type of "Part of Speech" in lowercaps like "noun" or "verb" (it's case sensitive)"""

    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        if data:
            meanings = data[0].get('meanings', [])
            if meanings:
                response_text = f"Definitions for {word}:\n\n"
                word_class_found = False
                for meaning in meanings: 
                    if word_class is not None and meaning['partOfSpeech'] == word_class:
                        word_class_found = True
                        response_text += f"Part of Speech: {meaning['partOfSpeech']} \n"
                        for definition in meaning['definitions']:
                            response_text += f"{definition['definition']} \n" 
                            response_text += "\n"
                    
                    elif word_class is not None and not word_class_found:
                        await message.send("Couldn't find the partofSpeech you wanted, check your spelling (Error: Word Class not Found)")
                    
                    else:     
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

@this.error
async def this_error(message, error):
    if isinstance(error, commands.CommandOnCooldown):
        await message.send(f""" As this command relies on interactions with external APIs to retrieve all the definitions, this cooldown is implemented to conserve resources and minimize the strain on this code. Thank you for our understanding. For you: ||<:CU_EeveeTease:850428169471393802>|| \n
                           This command is on cooldown. Please wait {error.retry_after:.2f} seconds.""")
    else:
        await message.send(f"Lmao you have the worst luck ever. (I'm sorry but) Here's the unique error you encountered: {error}")



##  ----------------------------------------------------- D E F I N E | W | S Y N S --------------------------------------------------------------- ##   
         

        
@define.command()
@app_commands.guilds(discord.Object(id = 773492566208675851))
@commands.cooldown(1, 60, commands.BucketType.user)
async def with_synonyms(message, word, word_class):
    url = f"https://www.wordhippo.com/what-is/another-word-for/{word}.html"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        synonyms_list = []
        word_types = []

        # Find all sections containing synonyms and their respective part of speech
        synonym_sections = soup.find_all('div', class_='relatedwords')
        for section in synonym_sections:
            word_type = section.find_previous(class_='wordtype').text.strip()
            word_type = word_type.replace('▲', '').strip()
            word_type = word_type.lower()

            # Check if word type is a valid part of speech
            if word_type in ['noun', 'verb', 'adjective', 'adverb', 'preposition', 'phrase', 'interjection']:
                word_types.append(word_type)
                if word_type == word_class:
                    synonyms = [a.text.strip() for a in section.find_all('a')][:10]  # Get first 10 synonyms
                    synonyms_list.append(synonyms)

        # Find definitions for each part of speech
        definitions = []
        definition_sections = soup.find_all('div', class_='tabdesc')

        for section in definition_sections:
            word_type = section.find_previous(class_='wordtype').text.strip()
            word_type = word_type.replace('▲', '').strip()
            word_type = word_type.lower()
            
            # Check if word type is a valid part of speech
            if word_type in ['noun', 'verb', 'adjective', 'adverb', 'preposition', 'phrase', 'interjection']:
                if word_type == word_class:
                    definition = [section.text.strip()]       
                    definitions.append(definition)
        # instead of name use index (1,2,3,4 etc for definition and synonym in this way response text would be easily formatted)
        if synonyms_list:
            response_text = f"Definition  of {word} \n"
            response_text += f"`{word_class}` \n"
            i = 1
            while i <= len(definitions):  
                response_text += f"{i}. Definition : {''.join(definitions[i-1])} \n   Synonyms: {', '.join(synonyms_list[i-1])} \n"
                i += 1
            await message.send(response_text)
        else:
            word_types1 = ",".join(word_types)
            await message.send(f"""No synonyms found for {word} within {word_class}.
                  => Here's all the word_class fetched for this {word}: \n {word_types1}""")
    else:
        await message.send(f"Failed to fetch synonyms for {word}. Status code: {response.status_code}")

@with_synonyms.error
async def synonyms_error(message, error):
    if isinstance(error, commands.CommandOnCooldown):
        await message.send(f""" As this command relies on interactions with external APIs to retrieve all the definitions & synonyms, this cooldown is implemented to conserve resources and minimize the strain on this code. Thank you for our understanding. For you: ||<:CU_SnorlaxLove:844161930712449034>|| \n
                           This command is on cooldown. Please wait {error.retry_after:.2f} seconds.""")
    else:
        await message.send(f"Lmao you have the worst luck ever. (I'm sorry but) Here's the unique error you encountered: {error}")


##  ------------------------------------------------------- D E F I N E | W | E X ------------------------------------------------------------------- ##

        
@define.command()
@app_commands.guilds(discord.Object(id = 773492566208675851))
@commands.cooldown(1, 60, commands.BucketType.user)
async def with_example(message, word, word_class: str=None):
    """Sends word definition with example. Specify word class (noun, verb, etc.) in lowercase'"""
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if data:
            meanings = data[0].get('meanings', [])
            if meanings:
                response_text = f"Definitions for {word}:\n\n"
                word_class_found1 = False
                for meaning in meanings:
                    if word_class is not None and  meaning['partOfSpeech'] == word_class:
                        word_class_found1 = True
                        response_text += f"Part of Speech: {meaning['partofSpeech']} \n"
                        for definition in meaning['definitions']:
                            response_text += f"Definition: {definition['definition']} \n"
                            if 'example' in definition:
                                response_text += f"Example: {definition['example']} \n"
                                response_text += "\n"
                    
                    elif word_class is not None and not word_class_found1:
                        await message.send("Couldn't find the partofSpeech you wanted, check your spelling (Error: Word Class not Found)")

                    else:
                        response_text += f"Part of Speech: {meaning['partOfSpeech']}\n"
                        for definition in meaning['definitions']:
                            response_text += f"Definition: {definition['definition']}\n"
                            if 'example' in definition:  # Checking if 'example' key exists
                                response_text += f"Example: {definition['example']}\n"
                                response_text += "\n"
                await message.send(response_text)
            else:
                await message.send(f"No definitions found for {word}.")
        else:
            await message.send(f"No data found for {word}.")
    else:
        await message.send(f"Failed to fetch data. Status code: {response.status_code}")

@with_example.error
async def example_error(message, error):
    if isinstance(error, commands.CommandOnCooldown):
        await message.send(f""" As this command relies on interactions with external APIs to retrieve all the definitions & example, this cooldown is implemented to conserve resources and minimize the strain on this code. Thank you for our understanding. For you: ||<:CU_UrCute:843903865237405706>|| \nThis command is on cooldown. Please wait {error.retry_after:.2f} seconds.""")
    else:
        await message.send(f"Lmao you have the worst luck ever. (I'm sorry but) Here's the unique error you encountered: {error}")

        
##  ------------------------------------------------------- O R I G I N ------------------------------------------------------------------- ##

@bot.hybrid_command(with_app_command=True)
@app_commands.guilds(discord.Object(id = 773492566208675851))
@commands.cooldown(1, 60, commands.BucketType.user)
async def origin(message, word):
    """get_etymology"""
    url = f"https://www.etymonline.com/word/{word}"
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response2 = requests.get(api_url)
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        reply = f"Origin of {word} \n"
        reply += soup.find("section", class_="word__defination--2q7ZH").get_text().strip()
        # print("This is the printed ans"+ans)
        
    elif response2.status.code != 200:
        reply = "Sorry, we couldn't find that word"
    else: 
        reply = "Sorry, We Couldn't find the origin of this word"
    await message.send(reply)

@origin.error
async def origin_error(message, error):
    if isinstance(error, commands.CommandOnCooldown):
        await message.send(f""" As this command relies on interactions with external APIs to retrieve the facts about the origin of the specified word, this cooldown is implemented to conserve resources and minimize the strain on this code. Thank you for our understanding. For you: ||<a:CU_GirlBang:926772990333575178>|| \nThis command is on cooldown. Please wait {error.retry_after:.2f} seconds.""")
    else:
        await message.send(f"Lmao you have the worst luck ever. (I'm sorry but) Here's the unique error you encountered: {error}")


## \--------------------------------------------------------------------------------------------------------------------------------------/ ##


#    /------------------------------------------- Q U O T E  | C O M M A N D S ------------------------------------------------------\


### Quote --> https://api.quotable.io/
        
##  ------------------------------------------------------- G R O U P ------------------------------------------------------------------- ##
    
@bot.hybrid_group(name = "quote", with_app_command=True)
@app_commands.guilds(discord.Object(id = 773492566208675851))
async def quote(message):
    await message.send("Es lo que es")

##  ------------------------------------------------------- R A N D O M ------------------------------------------------------------------- ##

@quote.command(with_app_command=True)
@app_commands.guilds(discord.Object(id = 773492566208675851))
@commands.cooldown(1, 5, commands.BucketType.user)
async def random(message):
    """Sends a random quote"""
    url = "https://api.quotable.io/quotes/random"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # print(data[0])
        # print(data[0]['content'])
        Genre = ", ".join(data[0]["tags"])
        reply = f"<a:CU_Starz:926772874759503903>     **Genre**: `{Genre}` \n \n"
        reply += f"<a:CU_WhiteArrow:926772858259132436>     \"{data[0]['content']}\" - {data[0]['author']}"
    else:
        reply = f"Sorry something went wrong: [Error: {response.status.code}]"
    await message.send(reply)

@random.error
async def random_error(message, error):
    if isinstance(error, commands.CommandOnCooldown):
        await message.send(f""" As this command relies on interactions with external APIs to retrieve quotes, this cooldown is implemented to conserve resources and minimize the strain on this code. Thank you for our understanding. For you: ||🕵🏻‍♂️🍃|| \nThis command is on cooldown. Please wait {error.retry_after:.2f} seconds.""")
    else:
        await message.send(f"Lmao you have the worst luck ever. (I'm sorry but) Here's the unique error you encountered: {error}")

##  ---------------------------------------------------- G E N R E | B A S E D --------------------------------------------------------------- ##

@quote.command(with_app_command = True)
@app_commands.guilds(discord.Object(id = 773492566208675851))
@commands.cooldown(1, 5, commands.BucketType.user)
async def genre(message, genre: str):
    """Sends a quote of the specified genre"""
    url = f"https://api.quotable.io/quotes/random?tags={genre}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        Genre = ", ".join(data[0]["tags"])
        reply = f"<a:CU_Starz:926772874759503903>     **Genre**: `{Genre}` \n \n"
        reply += f"<a:CU_WhiteArrow:926772858259132436>     \"{data[0]['content']}\" - {data[0]['author']}"
    else:
        reply = "Apologies, the genre you've provided isn't recognized. Please select a valid genre."
    
    await message.send(reply)

@genre.error
async def genre_error(message, error):
    if isinstance(error, commands.CommandOnCooldown):
        await message.send(f""" As this command relies on interactions with external APIs to retrieve quotes, this cooldown is implemented to conserve resources and minimize the strain on this code. Thank you for our understanding. For you: ||🍪|| \nThis command is on cooldown. Please wait {error.retry_after:.2f} seconds.""")
    else:
        await message.send(f"Lmao you have the worst luck ever. (I'm sorry but) Here's the unique error you encountered: {error}")

##  ------------------------------------------------------ T A G S ------------------------------------------------------------------ ##
        
@quote.command(with_app_command = True)
@app_commands.guilds(discord.Object(id = 773492566208675851))
@commands.cooldown(1, 60*5, commands.BucketType.user)
async def tags(message):
    """Retrieves a list of all available "valid" genres of quotes."""
    url = "https://api.quotable.io/tags"
    response = requests.get(url)
    genre = []
    if response.status_code == 200:
        data = response.json()
        tags = [tag["name"] for tag in data]
        for item in tags:
            if item not in genre:
                genre.append(item)
        response_text = "Here's a list of all available \"valid\" genre of quotes \n"
        i = 1
        while i<= len(genre):
            response_text += f"`{i}.` {genre[i-1]} \n"
            i += 1
        reponse_text += "**Please note**: Many of the listed tags may have only a few quotes or none at all."
        await message.send(response_text)
    

@tags.error
async def tags_error(message, error):
    if isinstance(error, commands.CommandOnCooldown):
        await message.send(f""" As this command relies on interactions with external APIs to retrieve tag information, this cooldown is therefore implemented to conserve resources and minimize the strain on this code. Thank you for understanding.  For you:  ||<:CU_Bear:926755755804201020>||\nThis command is on cooldown. Please wait {error.retry_after:.2f} seconds.""")
    else:
        await message.send(f"Lmao you have the worst luck ever. (I'm sorry but) Here's the unique error you encountered: {error}")

## \--------------------------------------------------------------------------------------------------------------------------------------/ ##

#    /------------------------------------------- C H A I N  | C O M M A N D S ------------------------------------------------------\


### Word Games --> https://dictionaryapi.dev
        
##  ------------------------------------------------------ G R O U P ------------------------------------------------------------------- ##

# Word Chain  # (ye we know)
@bot.hybrid_group(name = "chain", with_app_command=True)
@app_commands.guilds(discord.Object(id = 773492566208675851))
async def chain(message):
    await message.send("Tie me up daddy!")



@chain.command(name = "info", aliases = [ "Info"])
@app_commands.guilds(discord.Object(id=773492566208675851))
@commands.cooldown(1,300,commands.BucketType.user)
async def info(message):
    """Information about Word Chain Game""" 
    member = message.author
    pfp = member.display_avatar
    embed = discord.Embed(title= "Welcome to the Word Battle Arena!", colour=discord.Colour.red())
    embed.set_footer(icon_url="https://cdn.discordapp.com/emojis/844143267305226291.gif?size=80&quality=lossless", text="Have fun <3")
    embed.set_author(name= f"Salutations, {message.author}!", url = "https://discord.com/channels/773492566208675851/773503731177750548/1239455961937215580", icon_url=f"{pfp}")
    embed.add_field(name=f"***Information***", value=f"""\n<a:CU_Starz:926772874759503903>     In this noble battleground of lexicons, warriors clash in a test of linguistic prowess!
<a:CU_Starz:926772874759503903>     Prepare your arsenal of words and embark on a journey where valour is measured by the letters you wield.\n
          <a:CU_WhiteArrow:926772858259132436> **To Commence the Battle**: Summon the spirits of the arena with `w.chain start` (or use slash commands) within our esteemed battle hall (<#787193334988931082>).
          <a:CU_WhiteArrow:926772858259132436> **Participating in the Fray**: Join the ranks of champions by submitting a word that continues the storied chain.
          <a:CU_WhiteArrow:926772858259132436> **Forbidden Lexicons**: Beware! Dishonourable words are banned from this arena.
          <a:CU_WhiteArrow:926772858259132436> **Victorious Triumph**: The battle ceases upon the stalemate of silence.\n""")
    embed.add_field(name="*May your words echo through history as you engage in this **epic clash of vocabulary**!*", value = "", inline=False)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/865310876319612935/1239481704012582914/New_Project.png?ex=664314ca&is=6641c34a&hm=5830eb7373705d7d34137bcb41288b0da19c415383ebefc09f6c2669711823d1&")
    embed.timestamp = datetime.datetime.now()  # Sets the current time as the timestamp

    await message.send(embed= embed)

@chain.command(name = "rule", aliases = ["help", "Help", "Rule", "rules", "Rules"])
@app_commands.guilds(discord.Object(id=773492566208675851))
@commands.cooldown(1,3,commands.BucketType.user)
async def rules(message):
    """Rules of the Word Chain"""
    member = message.author
    pfp = member.display_avatar
    embed = discord.Embed(title= "Welcome to the Word Battle Arena!", colour=discord.Colour.red())
    embed.set_footer(icon_url="https://cdn.discordapp.com/emojis/844143267305226291.gif?size=80&quality=lossless", text="Have fun <3")
    embed.set_author(name= f"Salutations {message.author}!", url = "https://discord.com/channels/773492566208675851/773503731177750548/1239455961937215580", icon_url=f"{pfp}")
    embed.add_field(name = "***Rules of the Arena***", value = """\n`1.` **Objective**: Word Chain is a game where players take turns coming up with words that begin with the last letter of the previous word.
`2.` **Gameplay**: Players must think of a word that starts with the letter that the previous word ended with. For example, if the previous word is "apple", the next word could be "elephant".\n     e.g: `"appl(e)" → "elephan(t)" → "tige(r)" → "rabbit" & so on.`
`3.` **Word Restrictions**: Use valid English words recognized by the dictionary, avoiding repetition. Valid words get a tick emoji reaction from the bot.
`4.` **Conversational Symbols**: Begin your messages with symbols like "!", ".", or ">" to chat without affecting the game.\n     eg. `.Wassup Dumb Cat`
`5.` **End of Game**: The game lasts until a stalemate, with the winner being the last to contribute a valid word.""", inline=False)
    embed.add_field(name="*May your words echo through history as you engage in this **epic clash of vocabulary**!*", value = "", inline=False)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/865310876319612935/1239481704012582914/New_Project.png?ex=664314ca&is=6641c34a&hm=5830eb7373705d7d34137bcb41288b0da19c415383ebefc09f6c2669711823d1&")
    embed.timestamp = datetime.datetime.now()  # Sets the current time as the timestamp

    await message.send(embed = embed)

##  ------------------------------------------------------ S T A R T ------------------------------------------------------------------- ##
    
@chain.command(with_app_command=True)
@app_commands.guilds(discord.Object(id = 773492566208675851))
async def start(message):
    global word_game_on, desired_channel, last_letter
    if message.author.guild_permissions.manage_messages and word_game_on == False:
        word_game_on = True
        desired_channel = message.channel
        last_letter = chaos.choice('abcdefghijklmnopqrstuvwxyz')
        await message.send(f"""Prepare yourselves, warriors! The ultimate word battle is about to commence in {desired_channel.mention}. \nLet the war of words begin! Our first letter is: {last_letter.upper()}""")
    elif word_game_on:
        await message.send("The word battle has already commenced")
    else:
        await message.send("Hark, noble patrons! Only those bearing the esteemed title of CU Staff may unleash the game's fury upon this arena.")
        await asyncio.sleep(5)
        await message.channel.purge(limit=1)

##  ------------------------------------------------------ E N D ------------------------------------------------------------------- ##
        
@chain.command(with_app_command=True)
async def end(message):
    global word_game_on, desired_channel, previous_word, used_words
    if message.author.guild_permissions.manage_messages:
        if word_game_on == True:
            desired_channel = None
            word_game_on = False
            previous_word = None
            used_words = {}
            await message.send("Farewell, challengers! Your words rang with the resonance of valor. The command, or one of equal stature, has decreed an end to this noble battle. \n**Until we meet again in the arena of words**!")
        
        else:
            await message.send("You obtuse commander! The contest has scarcely commenced, and already you bid it cease? What cowardice!")
    else:
        await message.send("You lack the stature (permission) to decree an end to the battle!")

## \--------------------------------------------------------------------------------------------------------------------------------------/ ##


# Count -> math module (lmao just kiddin)

@bot.hybrid_group(name = "count", with_app_command=True, aliases = ["Count", "Numbers", "mafs", "ct"])
@app_commands.guilds(discord.Object(id = 773492566208675851))
async def count(message):
    """ Mafs or something i dunno """
    response_text = "The mathematics isn't adding up, my friend."
    message.send(response_text)


@count.command(name = "info", aliases = ["help", "Help", "Info"])
@app_commands.guilds(discord.Object(id=773492566208675851))
@commands.cooldown(1,300,commands.BucketType.user)
async def info(message):
 
    embed = discord.Embed(title="Welcome to the Word Battle Arena!", description="In this noble battleground of lexicons, warriors clash in a test of linguistic prowess! Prepare your arsenal of words and embark on a journey where valor is measured by the letters you wield.\n🔹 **To Commence the Battle:** Summon the spirits of the arena with \`!start\` within our esteemed battle hall. \n🔹 **Participating in the Fray:** Join the ranks of champions by submitting a word that continues the storied chain.\n🔹 **Forbidden Lexicons:** Beware! Dishonorable words are banned from this arena.\n🔹 **Victorious Triumph:** The battle ceases upon the repetition of a word or the stalemate of silence.\n\nMay your words echo through history as you engage in this epic clash of vocabulary!", colour=discord.Colour.red())
    embed.set_footer(icon_url="https://cdn.discordapp.com/emojis/844143267305226291.gif?size=80&quality=lossless", text="In the spirit of valiant word duels, revel in the fray! (<3)")
    embed.set_author(name = f"Hey, {message.author}", url = "https://discord.com/channels/773492566208675851/773503731177750548/1238976852501201038", icon_url="https://cdn.discordapp.com/attachments/865310876319612935/1239006563784458322/WordBot1.png?ex=66415a48&is=664008c8&hm=47cd1a96df9ac9935900e51c2e592ca7b7877e81eec5d975bae961eb9ec8367f&")
    embed.timestamp = datetime.datetime.now()  # Sets the current time as the timestamp
    embed.add_field(name="Field Title", value="*Italic text* **Bold text** __Underlined text__", inline=False)
    embed.add_field(name="Field Title", value=f"Mentioning user: <@{message.author.id}>", inline=False)
    embed.add_field(name="Field Title", value="<:emoji_name:emoji_id> This is a custom emoji", inline=False)



    await message.send(embed= embed)


@count.command(name="start", aliases=["st","Start", "Begin", "begin", "Commence", "commence", "Initiate", "initiate", "Embark", "embark"])
@app_commands.guilds(discord.Object(id=773492566208675851))
async def start(message, channel: discord.TextChannel=None):
    global count_on, count_channel, count_number, count_respondent_id
    if channel == None:
        channel = message.channel
    if message.author.guild_permissions.manage_messages and count_on == False:
        count_on = True
        count_channel = channel
        count_number = 0
        count_respondent_id = None
        await message.send(f"Make ready, esteemed comrades! The grand arithmetic odyssey is upon us in {count_channel.mention}. Let the enumeration embark! Our initial numeral stands thus: ||1||.")
    elif count_on:
        await message.send("The tally hath already started.")
        await asyncio.sleep(5)
        await message.channel.purge(limit=1)
    else:
        await message.send("Attend, esteemed patrons! Only those endowed with the revered status of CU Staff may unleash the fervor of counting upon the populace.")
        await asyncio.sleep(5)
        await message.channel.purge(limit=1)



@count.command(name = "end", aliases =['ed', "End", 'stop', "Stop"])
@app_commands.guilds(discord.Object(id=773492566208675851))
async def end(message):
    global count_on, count_channel, count_number, count_respondent_id
    if message.author.guild_permissions.manage_messages:
        if count_on == True:
            count_channel = None
            count_on = False
            count_number = 0
            count_respondent_id = None
            await message.send("Fare thee well, intrepid adventurers! Thy numerals resound with the echoes of scholarly pursuit. The edict, or one of commensurate station, hath decreed the conclusion of this erudite expedition. \n**Until our paths converge once more amidst the realms of numerical pursuit!**")
        
        else:
            await message.send("Thou obtuse director! The quest hath scarce commenced, and yet thou dost command its cessation? What trepidation!")
    else:
        await message.send("Thou lackest the station (permission) to adjudge an end to our scholarly pursuit!")




# Boom -> copy past count but more boring


# One Word Story -> wordhippo


# Hangman (possible?) - yes - https://youtu.be/0G3gD4KJ59U (TurkeyDev)



######
@bot.hybrid_command
async def test(message, member: discord.Member = None):
    if member is None:
        member = message.guild.get_member(bot.user.id)  # Get the bot member object
    
    name = member.display_name
    pfp = member.display_avatar
    icon = member.display_name


    embed = discord.Embed(title = "Title", description = "Description", colour = discord.Colour.random()) #or you can use discord.Color.random()
    embed.set_author(name = f"{name}", url = "https://discord.com/channels/773492566208675851/773503731177750548/1238976852501201038", icon_url="https://cdn.discordapp.com/attachments/865310876319612935/1239006563784458322/WordBot1.png?ex=66415a48&is=664008c8&hm=47cd1a96df9ac9935900e51c2e592ca7b7877e81eec5d975bae961eb9ec8367f&")
    embed.set_thumbnail(url = f"{pfp}")
    embed.add_field(name= "Field 1", value = "Value of the Field")
    embed.add_field(name= "Field 2", value = "Value of the Field with inline true", inline=True)
    embed.add_field(name= "Field 3", value = "Value of the Field with inline fale", inline = False)
    embed.set_footer(text="**This is the footer**", icon_url= "https://en.wikipedia.org/wiki/History_of_calendars")
    embed.timestamp
    await message.send(embed = embed)

# Command to play the game
        
@bot.event
async def on_message(message):
    global last_letter, word_game_on, desired_channel, previous_word, word_respondent_id
    global count_channel, count_on, count_respondent_id, count_number
    # command = message.content.split()[0]
    # args = message.content.split()[1:0]

    
    if message.author == bot.user:
        return 
    
    ## Check if the message is a command
    await bot.process_commands(message)

    ## Game Code

    if word_game_on:
        # if message.content == 'w.end':
        #     return
        if message.author == bot.user:
            return
        if message.channel != desired_channel:
            return
        
        if message.channel == desired_channel:
            if message.author == bot.user or message.content.startswith(('!', '.', '>', "w.")):
                return
            else:
                if message.author.id == word_respondent_id:
                    await message.delete()
                    await message.channel.send(f"Verily {message.author.mention}, you may not monopolize all the words! Permit other participants to revel in the merriment as well.")
                    await asyncio.sleep(5)
                    await message.channel.purge(limit=1)
                
                elif not message.content.lower().startswith(last_letter):
                    await message.delete()
                    await message.channel.send(f"{message.author.mention}, your word lacks valor! Commence with a word that befits the letter **{last_letter.upper()}**.")
                    await asyncio.sleep(5)
                    await message.channel.purge(limit=1)

                elif message.content.lower().startswith(last_letter) and len(message.content) > 1 and message.author.id != word_respondent_id:
                    
                    word = message.content.lower()

                    if word in used_words:
                        await message.delete()
                        await message.channel.send(f"This word, \"{word},\" hath already been wielded by {used_words[word]}.")
                    
                    elif word in prohibited_words:
                        await message.delete()
                        await message.channel.send("**This word is forbidden**! How dare thee employ such vile terms in this noble contest?")
                        await asyncio.sleep(5)
                        await message.channel.purge(limit=1)
                        
                    else:
                        # Check if the word is in the Oxford dictionary (simplified check) (becoz i didn't know anythin back then)
                        url1 = f"https://www.wordhippo.com/what-is/another-word-for/{word}.html"
                        url2 = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
                        response = requests.get(url1)
                        response_2 = requests.get(url2)
                        # Double checking coz why not (the ol' wordbot had an outdated dictionary to play with that's why the double check)
                        if response.status_code == 200 or response_2.status_code == 200:
                            emoji = "<:CU_Accept:866720792578359317>"
                            await message.add_reaction(emoji)  # React with a checkmark emoji
                            last_letter = word[-1]  # Update the last letter
                            previous_word = word   # Pretty sure this variable is just useless but i don't want to break the game
                            word_respondent_id = message.author.id
                            used_words[word] = word_respondent_id
                        else:
                            await message.channel.send("Apologies, that word doth not dwell within the annals of the lexicon. Seeketh another, I pray thee.")
    
    if count_on:
        if message.author == bot.user:
            return
        if message.channel != count_channel:
            return
        
        if message.channel == count_channel:
            if message.author == bot.user or message.content.startswith(('!', '.', '>', "w.")):
                return
            else:
                if message.content.isdigit():
                    if message.author.id == count_respondent_id and message.content.isdigit():
                        await message.delete()
                        await message.channel.send(f"Verily {message.author.mention}, you foul scholar who dare revel all by himself in the domain of numbers")
                        await asyncio.sleep(5)
                        await message.channel.purge(limit=1)
                    elif int(message.content) != (count_number+1):
                        await message.channel.send(f"{message.author.mention}, your calculations are off fellow scholar, I urge you to think of the number that succeds **{count_number}**.")
                        await message.delete()
                        await asyncio.sleep(5)
                        await message.channel.purge(limit=1)
                    elif int(message.content) == (count_number+1) and message.author.id != count_respondent_id:
                        emoji = "<:CU_Accept:866720792578359317>"
                        meme_no = [4, 7, 13, 20, 21, 24, 25, 15,39,42, 64, 69, 74, 76, 123, 365, 404, 420, 666, 911, 1234, 1337, 1984, 2012, 2077, 9000, 117013, 58008, 5318008]
                        if (count_number+1)>100:
                            emoji1 = ""
                        elif (count_number+1) in 
                        # elif (count_number+1) == 69 or expected_number
                        emoji1 = "<:CU_EchindaNote:843903863492837476>"
                        await message.add_reaction(emoji)
                        await message.add_reaction(emoji1)
                        count_number += 1
                        count_respondent_id = message.author.id
                else:
                    await message.channel.send(f"Nah uh! {message.author.mention} you dare seek to abandon our quest for numerical dominion")
                    await asyncio.sleep(5)
                    await message.channel.purge(limit=1)


    
    if story_on:
        return 








bot.run('MTIxNjQ1MTg5OTM2OTMyODY2MA.GcxPoO.wewF3pKNIsvelEXwOZLE5SiMuefb12IJoGzZhY')
