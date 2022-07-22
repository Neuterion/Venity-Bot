# Import basic libraries that will help get & modify data
from playersearch import playerSearch
from guildsearch import guildSearch, get_guild_members
from lbsearch import drawLB
from statsearch import statSearch
from searchlib import webText, isdigit

# Basic libraries for discord.py
import discord
from discord.ext import commands

# Sets the bot so that it gets called when using its' prefix or it's mentioned when using a command
bot = commands.Bot(command_prefix=commands.when_mentioned_or('vn!'))

# Removes the bots' default help command
bot.remove_command('help')


# Changes bots' Discord activity and prints a message when ready to use
@bot.event
async def on_ready():
    print(f"{bot.user} is ready!")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply("You are missing permission(s) to run this command. This bot needs these permissions: ```send_messages, attach_files, embed_links```.", mention_author=False)
    elif isinstance(error, discord.errors.Forbidden):
        await ctx.reply("You might have disabled the 'embed links' permission for this bot.", mention_author=False)
    elif isinstance(error, commands.errors.CommandNotFound):
        await ctx.reply("Invalid command! Type vn!help for more information.", mention_author=False)
    else:
        raise error


# Help command that can be used to get help for a certain command
@bot.group(invoke_without_command=True)
async def help(ctx):
    log(ctx)
    # Create list of available commands and send them as an embedded message (default)
    em = discord.Embed(title="Help", description="Use vn!help [command] for more info!", color=ctx.author.color)
    em.add_field(name="Player Search", value="player, lb, stats")
    em.add_field(name="Guild Search", value="guild")

    await ctx.reply(embed=em, mention_author=False)


# Help command for vn!player command
@help.command()
async def player(ctx):
    log(ctx)
    await ctx.send(embed=discord.Embed(title="player", description="Used to lookup player data.\nUsage: vn!player [player]",
                                       color=ctx.author.color))


# Help command for vn!guild command
@help.command()
async def guild(ctx):
    log(ctx)
    await ctx.reply(embed=discord.Embed(title="guild", description="Used to lookup guild data.\nUsage: vn!guild [guild name]",
                                       color=ctx.author.color), mention_author=False)


# Help command for vn!stats command
@help.command()
async def stats(ctx):
    await getStatNames(ctx, "stats [gamemode] [player]")


# Help command for vn!lb command
@help.command()
async def lb(ctx):
    await getStatNames(ctx, "lb [gamemode] [page]")


# Used to search a players' general statistics
@bot.command()
async def player(ctx, *, player=''):
    log(ctx)
    if await maintenance(ctx):
      return

    # Check if user didn't enter any name
    if player == '':
        return await ctx.reply("Please enter a players' name. Usage: vn!player [player]", mention_author=False)

    # Lowercase and strip the players' name (user-friendly)
    player = player.strip('" ')

    # Get HTML file for the players' webpage
    playerText = webText(f"player/{player}")

    # Check for valid name
    if len(playerText.select('td[class=col-xs-9]')) == 0:
        # Ensure user entered a valid player
        return await ctx.reply('Invalid player!', mention_author=False)
    else:
        # Send data
        await ctx.reply(file=playerSearch(playerText), mention_author=False)


# Used to search a guilds' statistics
@bot.command()
async def guild(ctx, *, guild: str = ''):
    log(ctx)
    if await maintenance(ctx):
        return
    
    embed = guild

    # Check if user didn't enter a valid guild name
    if guild == '':
        return await ctx.reply("Please enter a valid guild name. Usage: vn!guild [guild]", mention_author=False)

    # Lowercase and strip the guilds' name (user-friendly)
    guild = guild.strip('" ')

    # Get HTML file for the guilds' webpage
    guildText = webText(f"guild/{guild}")

    # Check for valid name
    if len(guildText.select('td[class=col-xs-9]')) == 0:
        return await ctx.reply("Invalid guild (try searching by its' name, not tag if you haven't). Usage: vn!guild [guild]", mention_author=False)
    else:
        # Send data
        await ctx.reply(file=guildSearch(guildText), mention_author=False)


@bot.command()
async def members(ctx, *, guild: str = ''):
    log(ctx)
    
    if await maintenance(ctx):
        return
    
    # Lowercase and strip the guilds' name (user-friendly)
    guild = guild.strip('" ')
    
    embed = get_guild_members(ctx, guild)
    
    # Check if user didn't enter a valid guild name
    if guild == '' or embed == None:
        return await ctx.reply("Please enter a valid guild name. Usage: vn!guild [guild]", mention_author=False)
        
    await ctx.reply(embed=embed, mention_author=False)


# Used to search a leaderboard by a certain stat
@bot.command()
async def lb(ctx, stat: str = '', page="1"):
    log(ctx)

    if not page.isnumeric():
        return await ctx.reply("Please specify a page, not text.", mention_author=False)

    page = int(page)

    if await maintenance(ctx):
      return

    # Check if user didn't enter a stat
    if stat == '':
        return await ctx.reply("Invalid usage. Usage: vn!lb [stat] [page]", mention_author=False)

    # Lowercase and strip the stat name (user-friendly)
    stat = stat.strip(" ").lower()

    # Create dictionary of stat names and their page name on the website
    statTypes = {
        "bw1": "bw-solo-win", "bw2": "bw-doubles-win", "bw3": "bw-3v3v3v3-win", "bw4": "bw-4v4v4v4-win",
        "sw1": "sw-solo-kill", "sw2": "sw-doubles-kill",
        "tb1": "tb-solo-win", "tb2": "tb-doubles-win",
        "duels": "duels-win",
        "tntrun": "tntrun-win"
    }
    generalStatTypes = {"guild": "guild-level", "elo": "elo", "playtime": "playtime", "level": "level"}

    # Check if user entered a valid stat
    if stat in [*statTypes]:
        lbText = webText(f"leaderboard/{statTypes[stat]}")
    elif stat in [*generalStatTypes]:
        lbText = webText(f"leaderboard/{generalStatTypes[stat]}")
    else:
        return await ctx.send(embed=statErr(ctx, command='lb'))

    # Check if user passed an invalid page
    if page * 10 > len(lbText.select('tr > td[class=col-xs-3]')) or page < 1:
        if page * 10 - len(lbText.select('tr > td[class=col-xs-3]')) >= 10 or page < 1:
            return await ctx.reply(embed=discord.Embed(title="Invalid Page", description="You might have went too far..", color=ctx.author.color), mention_author=False)
        else:
            limit = len(lbText.select('tr > td[class=col-xs-3]'))
    else:
        limit = page * 10

    # Web-scrape the names on the LB and the statistics
    nameLB = [i.contents for i in lbText.select('tr > td > a')[page * 10 - 10:limit]]
    statLB = [i.get_text() for i in lbText.select('tr > td[class=col-xs-3]')[page * 10 - 10:limit]]

    # Send data returned from the drawLB function
    await ctx.reply("Warning: Data displayed is likely to be outdated.", file=drawLB(lbText, page, nameLB, statLB, mode=stat), mention_author=False)


# Used to search a players' certain gamemode stats
@bot.command()
async def stats(ctx, gm='', *, player=''):
    log(ctx)
    if await maintenance(ctx):
      return

    # Check if user didn't pass all arguments
    if player == '' or not gm.isnumeric():
        return await ctx.reply("Invalid usage. Usage: vn!stats [gamemode] [player]", mention_author=False)

    # Lowercase and strip the gamemodes' name (user-friendly)
    gm = gm.strip().lower()

    # Get HTML file for the players' webpage
    playerText = webText(f"player/{player}")

    # Check for valid name
    if len(playerText.select('td[class=col-xs-9]')) == 0:
        # Ensure user entered a valid player
        return await ctx.reply('Invalid player!', mention_author=False)

    # Get BytesIO object of the PIL image
    IMG = statSearch(gm[:2] if isdigit(gm) else gm, gm[2] if isdigit(gm) else 1, playerText)

    # Check if user entered an invalid gamemode
    if IMG == False:
        return await ctx.reply(embed=statErr(ctx), mention_author=False)
    else:
        await ctx.reply(file=IMG, mention_author=False)


@bot.command()
@commands.is_owner()
async def die(ctx):
    await ctx.bot.logout()


# Returns a Discord embed with types of statistics that can be used for the stats & lb command
async def getStatNames(ctx, usage):
    log(ctx)
    em = discord.Embed(title="Stats", description=f"Used to lookup gamemode data.\nUsage: vn!{usage}", color=ctx.author.color)
    em.add_field(name="BedWars Modes", value="bw1, bw2, bw3, bw4")
    em.add_field(name="SkyWars Modes", value="sw1, sw2", inline=False)
    em.add_field(name="TheBridge Modes", value="tb1, tb2", inline=False)
    em.add_field(name="Duels Mode", value="duels", inline=False)
    em.add_field(name="TNTRun Mode", value="tntrun", inline=False)
    em.add_field(name="Other (lb cmd only)", value="guild (guild level), playtime, elo, level (player level)", inline=False)

    await ctx.reply(embed=em, mention_author=False)


# Returns a Discord embed that alerts a user when passing an invalid gamemode (for stats & lb command only)
def statErr(ctx, command='stats'):
    return discord.Embed(title="Invalid mode!", description=f"For more info, type 'vn!help {command}'", color=ctx.author.color)


async def maintenance(ctx):
    if len(webText("player/calmdusk").select('td[class=col-xs-9]')) == 0:
      await ctx.reply("player.venitymc.com is down right now!", mention_author=False)
      return True
    return False


def log(ctx):
    print(f"{ctx.message.author} ran the command '{ctx.message.content}' in '{ctx.message.guild.name}'")


# Pass the tokens' bot and run it
bot.run("OTE1MDUxNzM0NzU2MzcyNTAw.YaV-Vg.HWr90PgoIuEg-GWvP2sX9ptQ3d0")