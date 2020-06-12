import os, requests, re, time, json, random
from jikanpy import Jikan, AioJikan
import discord
from discord.ext import commands, tasks
import youtube_dl

from dotenv import load_dotenv

jikan = Jikan()

load_dotenv()

TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix='zz ')

bot.remove_command('help')


def yt_util(query):
    res = requests.get("https://www.youtube.com/results?search_query="+query)

    # p = re.finditer('/watch?', res.text)

    p = res.text

    x= p.find('/watch?')

    make = ''
    check = ''
    # print (x)

    while check != "\"":
        make = make +check
        check = p[x]
        x = x+1

    # print('https://www.youtube.com'+make)

    final = 'https://www.youtube.com'+make

    return final


@bot.event
async def on_ready():
    print (f'{bot.user} has connected to Discord!', end=" ")
    
    # for guild in client.guilds:
    #     i = guild.name
    #     print (i, end=" ")
    #     for member in guild.members:
    #         print(member.name, end=" ")
    print()

@bot.event
async def on_member_join(member):
    for i in member.guild.text_channels:
        if i.name=='general':
            await i.send(f'Welcome **{member.name}**')
    print()
    
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.find("<@!697817688566792223>") != -1:
        await message.channel.send(f"I don't like tags")

    await bot.process_commands(message)

# read up bot.check and on_command_error in Bot api

@bot.command(name="anime")
async def find_anime(ctx, *args):

    query = ''
    for i in args:
        query = query + i + ' '
    anime = jikan.search('anime', query)
    anime = anime['results'][0]
    req = jikan.anime(anime["mal_id"])
    # print (anime["mal_id"])

    # print(query)

    embed = discord.Embed(color=discord.Color.from_rgb(46,139,87))

    embed.title = req['title']
    embed.description = req['synopsis']

    # embed.add_field(name="Title", value=req['title'], inline= False)
    embed.set_image(url = req["image_url"])
    # embed.add_field(name="Description", value=req["synopsis"], inline=False)
    embed.add_field(name="Score", value = req['score'], inline= False)

    
    # await ctx.send(anime['image_url'] + "\n" + anime['url'])
    await ctx.send(embed = embed)
    # print(anime)

@bot.command(name='help')
async def help(ctx):
    embed=discord.Embed()
    embed.color = discord.Color.from_rgb(46,139,87)
    embed.title = "Zebras Guide"
    embed.set_thumbnail(url = 'https://media.gettyimages.com/videos/animated-hypnotic-tunnel-with-white-and-black-stripes-digital-loop-video-id1205926321?s=640x640')
    embed.description = "Use 'zz' to trigger commands. Here are the currently available commands. More might be on the way."
    embed.add_field(name="Anime", value ="Find an anime on MAL \n zz anime <query>", inline=False)
    embed.add_field(name="Youtube Search", value="Search for videos on Youtube \n zz yt <query>", inline=False)
    await ctx.send(embed=embed)

@bot.command(name='yt')
async def yt_scrape(ctx, *args):
    query = ''
    for i in args:
        query = query + i + '+'
    query = query[:-1]
    # print (query)

    final = yt_util(query)
    
    # res = requests.get("https://www.youtube.com/results?search_query="+query)

    # # p = re.finditer('/watch?', res.text)

    # p = res.text

    # x= p.find('/watch?')

    # make = ''
    # check = ''
    # # print (x)

    # while check != "\"":
    #     make = make +check
    #     check = p[x]
    #     x = x+1

    # # print('https://www.youtube.com'+make)

    # final = 'https://www.youtube.com'+make

    await ctx.send(final)
    
    # print (len(p))
    # print (res.text)

@bot.command(name='trivia')
async def trivia(ctx):
    # if ctx.guild.name != "matrix":
    #     await ctx.send("Not available here")
    #     return



    questions = []
    with open('ques.json', 'r') as f:
        content = f.read()
        questions = json.loads(content)["questions"]
        # print (questions)
        
    channel = ctx.channel
    await ctx.send("Let's begin the quiz or whatever")


    for i in range(4):
        wait = time.time()+3
        while time.time()<wait:
            pass
        p = random.randint(0,3-i)
        # print(i, questions)
        question = questions[p]["question"]
        answer = questions[p]["answer"]
        questions.pop(p)
        kill =0
        await ctx.send("Question "+str(i+1)+": "+question)
        check = time.time() + 10
        while time.time() < check:
            async for message in channel.history(limit=2):
                if message.content.lower() == answer:
                    await ctx.send(message.author.name + " got it correct")
                    kill=1
                    break
            if kill ==1:
                if i==3:
                    await ctx.send("That's all the questions")
                else:
                    await ctx.send("Next question in 3 secs")
                break
        if (kill==0):
            await ctx.send("What a bunch of dum-dums")
            if i==3:
                await ctx.send("That's all the questions")
            else:
                await ctx.send("Next question in 3 secs")

    

    

    

# @bot.command(name='play')
# async def music(ctx, *args):
#     query = ''
#     for i in args:
#         query = query + i + '+'
#     query = query[:-1]

#     # final = yt_util(query)

#     author = ctx.author

#     # print (author.voice)

#     try:
#         if (author.voice):
#             vclient = await author.voice.channel.connect(timeout=60.0, reconnect=True)

#         else:
#             await ctx.send("Please connect to a voice channel!")
#             return 
#     except Exception as e:
#         print (e)
#         return


#     print ("HERE")

#     player = await vclient.create_yt

# @bot.command(name='dc')
# async def dc(ctx, *args):
#     if (bot.voice_clients!=[]):
#         for i in bot.voice_clients:
#             await i.disconnect(force=False)


    

bot.run(TOKEN)