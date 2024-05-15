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
bot = commands.Bot(command_prefix='$', intents=intent) # our command prefix can be changed

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

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
        response += f'\n **{value[0]} - {value[1]} - {value[2]}:** {key}'
    embed.description = response
    await ctx.send(embed=embed)

bot.run(TOKEN)
client.run(TOKEN)