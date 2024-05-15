import urllib.request, json 
import os
import discord
from AQ_spellFuncs import *
from dotenv import load_dotenv
from discord.ext import commands

with urllib.request.urlopen("https://raw.githubusercontent.com/Macarkeys/PFC_SpellReader/main/pfc-elemental-divine-psionic-spells.json") as url:
    spellData = json.loads(url.read())

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')



intent = discord.Intents.default()
intent.message_content = True
bot = commands.Bot(command_prefix='$', intents=intent)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

"""@bot.command(name='GetSpell')
async def getSpell(ctx, subBackground: str, spellGroup: str, spell: str):
    #Probably make this into a series of functions that will return the dictionary key for each one until the end
    #Use spell names instead of spell number since alot of magic has double numbers
    #Cleaning of the json file is needed. I think I'm going to switch stuff to common inputs, like replacing dashes and other things.
    #Format will be as such main function gets index of subbackground, spellgroup, and spell, as tuple
    #Subbackground will get index of spellgroup and spell as tuple from spellgroup
    #spellgroup get spell from spell function
    #All of these functions will pass indexes downward.
    b, g, s = subBackground.strip(), spellGroup.strip(), spell.strip()
    b = levenshteinSort(spellData, b, list(spellData.keys()))
    if b == None:
        await ctx.send(f"SubBackground '{subBackground}' not found")
        return None
    g = levenshteinSort(spellData, g, list(spellData[b].keys()))
    if g == None:
        await ctx.send(f"Spell Group '{spellGroup}' not found in '{b}'")
        return None
    s = levenshteinSort(spellData, s, list(spellData[b][g].keys()))
    if s == None:
        await ctx.send(f"Spell '{spell}' not found in '{b}' - '{g}'")
        return None

    embed = discord.Embed(colour=discord.Color.dark_red())
    embed.title = f'**{b} - {g} - {s}**'
    for key, value  in spellData[b][g][s].items():
        embed.add_field(name =key,value=value, inline=True)
    await ctx.send(embed=embed)"""

@bot.command(name='spell')
async def spell(ctx, spell: str):
    s =  spell.strip()
    b, g, s = levenshteinSearch(spellData, s)
    if s == None:
        await ctx.send(f"Spell '{spell}' not found")
        return None
    embed = discord.Embed(colour=discord.Color.dark_red())
    embed.title = f'**{b} - {g} - {s}**'
    for key, value  in spellData[b][g][s].items():
        embed.add_field(name =key,value=value, inline=True)
    await ctx.send(embed=embed)

@bot.command(name='tag')
async def tag(ctx, tagStr: str):
    #take dictionary tags and put them and the spell in a embed
    tagDict = getSpellTags(spellData, tagStr)
    response = ''
    embed = discord.Embed(colour=discord.Color.dark_red())
    embed.title = f'**Tag Search: {tagStr}**'
    link = ctx.message.jump_url
    for key, value in tagDict.items():
        response+= f'\n **{value[0]} - {value[1]} - {value[2]}:** {key}'
    embed.description = response
    await ctx.send(embed=embed)




@bot.command(name='GetSpellBook')
async def getSpellBook(ctx, *spellBookDicts):
    print(spellBookDicts)
    
bot.run(TOKEN)

#ToDo:
#First, finish following tutorial
#Second, add a command to access a specific spell. Input will likely be getSpell (or something) 'Subbackground name' 'Spell group' 'Spell or rate number'
#To use we will have to clean the name then check if the cleaned name is in each key then access that key then do the same for the next level
#Third, add a command to give out a txt file of each spell group.
#Will take arguments like this 'spell group rank' 'spell group rank' 'spell group rank'
#impliment a way to search by tag. Basically search each every spell effect for the tag 
""" Ex: getSpells 'Love 2'
----------Love----------
1 - Concern
    Time to cast: 2 rounds
    Resist Check: willing target
    Target: touch
    Duration: 1 + 1/F weeks
    Area: single target
    Effect: danger alert
    Desc: While under this spell, any time the target enters combat, 
    the caster hears an appropriate danger alert, no matter the distance 
    separating them.

2 - Devote
    Time to cast: 2 rounds
    Resist Check: willing target
    Target: touch
    Duration: 1 + 1/F weeks
    Area: single target
    Effect: danger alert
    Desc: While under this spell, any time the target enters combat, 
    the caster hears an appropriate danger alert, no matter the distance 
    separating them.
"""

client.run(TOKEN)