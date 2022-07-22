# Project: Venity Stats

## Video Demo: <https://youtu.be/sraRPm7kQj0>

### Description

#### Introduction

Hello world! For this final project I made a Discord bot that displays data from a Minecraft BE server called "Venity Network" provided by the owner of the server itself on an image via *web scraping*. There are four types of data that are supported by the bot, which are player general data, player game data, guild data, and leaderboard data.

#### Important Decisions

Before I disclose the details about the bots' commands and the types of data on the website, I would like to go through some of the decisions I made while developing the bot: the language used, the technique used, the motive, and the libraries used to support this final project of mine.

1. Programming Languages
   1. **Python** because I'm very familiar with it
   2. **OTF/TTF** because it's just necessary for determining the data text font
   3. **PNG** because it goes well with text
2. Technique
   1. I used *web scraping* instead of using an *API* because I didn't know at that time that there was an *API*, so I just went along with it
3. Motive
   1. Some people just enjoy looking at data put onto an image more than looking at table data on the website!
4. Libraries/Modules Used
   1. *BeautifulSoup4* for parsing a manipulable HTML file
   2. *PIL* for image manipulation
      1. **Image** for opening the provided templates and copying them onto a new blank image. Also for copying images from the internet onto an image
      2. **ImageDraw** for drawing text and shapes on an image
      3. **ImageFilter** to blur the templates when copying them onto a new image
      4. **ImageFont** to determine the font of the text that's going to be written on the image
      5. **ImageColor** to determine some of the texts' color (only the ones that are from the website)
   3. *requests* for requesting an HTML file; goes together with BS4
   4. *io - BytesIO* for converting a PIL image into a byte (BytesIO) object which Discord supports as a file format. Saves memory instead of having to save the image locally, get the directory, sending it through Discord, and finally deleting the image.
   5. *discord - File* for creating a File object that can be sent through Discord; goes together with a BytesIO object.
   6. *discord.ext - commands* for building a bot with commands

#### Data Types of Venitys' Website

For this bot, I have decided to only use four out of five types of data on the website, the fifth one being pie chart data; I tried pasting the chart data onto the image with Selenium (module), however it ended up being messy (size was indefinite and couldn't remove the transparent chart background).  
Here are the types of data that the bot supports and where the data comes from:

##### Player General Data

Found on player pages (i.e. <https://player.venitymc.com/player/calmdusk>)  
Consists of the players' name, head skin, guild tag (if they're in a guild), level & XP, playtime, coins, rank, guild, first join, and last seen.

![General Data](https://i.postimg.cc/9M6sQrGb/playerdata.png)

##### Player Game Data

Found on player pages (i.e. <https://player.venitymc.com/player/calmdusk>)  
Consists of the players' game data on every gamemode that exists on Venity Network (Bed Wars, Sky Wars, The Bridge, Duels, and TNT Run).

![Game Data](https://i.postimg.cc/d30ZDVw7/playergamedata.png)

##### Guild Data

Found on guild pages (i.e. <https://player.venitymc.com/guild/crown>)  
Consists of the guilds' name, tag, member count, leader, level & XP, and creation date & time.

![Guild Data](https://i.postimg.cc/WbCqbVK3/guilddata.png)

##### Leaderboard Data

Found on guild pages (i.e. <https://player.venitymc.com/leaderboard/playtime>)
Consists of the leaderboards' headers, names, and stats.

![Leaderboard Data](https://i.postimg.cc/sgWQM8dJ/lbdata.png)

### Program Files

#### searchlib.py

searchlib.py is a library that will provide many of the necessary functions needed to support each file that will get and provide one of the websites' data types.

##### font(size)

Creates an **ImageFont** object, which can then be used to determine a texts' font upon creation on an image. I am using a Minecraft font

##### bFont(size)

The bold version of font().

##### headSkin(link)

Takes a link to an image as an argument and returns a **BytesIO** object of the content of the GET request to said link.

##### webText(link)

Takes a link as an argument and returns text from the HTML file from the text of the GET request which can be manipulated with the *bs4* module to get certain data.

##### midPos(text_width)

Returns the starting X position of where some text is going to be drawn on the center of the image (formula: center / 2 - text_width / 2).

##### isdigit(string)

isdigit() is a boolean function that's used to check whether a string contains a digit.

##### delete(list, element)

delete() deletes every instance of an element in a list.

##### byte(PIL_img)

byte() is a function that returns a **discord.File** object of the **BytesIO** object of a **PIL** image. Used for sending files to Discord.

##### copyTemplate(template_name)

copyTemplate() returns a newly created **PIL** image that's a blurred copy of one of the templates in the *bgtemplates* folder and an **ImageDraw** object to said image (for drawing text and shapes).

##### drawName(nameData, drawTemplate, center, Ypos)

drawName() draws a players' or guilds' name on the center of the image and on the Y coordinate intended. An important thing to note is that at the start of the function, the nameData list gets delete()'d of any newline element; that is because whenever I get name data (subnames of the name and their color) from the website, sometimes newline characters get added to the list and I'm not so sure why.

##### drawLevel(webText, drawTemplate, center, gap=100, MAINHEADCOLOR="white", MAINSTATCOLOR="yellow", isplayer=True)

drawLevel() draws a level bar that displays the current players' or guilds' level and their current XP count.  

- The *isplayer* argument differentiates between player and guild name (due to the contrast of getting the level & XP data from the *webText* provided).
- The *gap* argument sets the gap between the bar and the bottom part of the image.
- The *MHC* and *MSC* argument sets the color of header text and statistic text.

##### drawHead(draw, template, webText, X1, Y1, X2, Y2)

drawHead() draws a frame with a players' head skin image attached to it. First I drew a black square, and pasted the head skin image on the center of the square, and after that I drew a white outline of the image; the outline came last because the image would stack on it and it wouldn't be visible if it came first, and the main purpose of the outline is just so that if the players' head color's black, they could tell where the tip of the head is, and if the color was white, then it also wouldn't matter because the outline is thin.

##### drawStat(draw, relPos, Ypos, text, size, col="white")

drawStat() is mainly used to draw statistic text on the left and right (*relPos* arg) part of the image, hence its' common association with for loops in helper files.

#### playersearch.py

Helper file for looking up a players' general data.

##### playerSearch(playerText)

playerSearch() looks up a players' general data by requesting HTML text from a players' page, extracting data from it, and then drawing it. I have decided to draw them the Pythonic way, which is by for loop.

#### statsearch.py

Helper file for looking up a players' game data.

##### statSearch(game, mode, playerText)

statSearch() looks up a players' data on a certain mode (*mode* arg) of a certain gamemode (*game* arg) and displays it on an image.

##### drawGameTitle(game: str, mode: str, drawTemplate)

This function draws the title of a statSearch() image; based on the gamemode and its' mode chosen, this function will use different types of color palettes when drawing the title. It's seperated from the statSearch() function because it just looks more neat that way.

#### guild.py

Helper file for looking up a guilds' data.

##### guildSearch(guildpage)

This function is similar to the playerSearch() function, except that it's for guilds and the *locations* of the extracted data are different.

#### lbsearch.py

Helper file for looking up leaderboard data.

##### drawLB(lbtext, page, nameLB, statLB, mode='')

drawLB() only extracts the leaderboard header texts and creates the rank numbers based on the *page* argument; the rest of the data is passed so we can just draw them by for loop. This design was chosen because manipulating the extracted leaderboard data is somewhat a bit easier for the caller than the callee.

##### drawHeader(draw, col1, col2, *headers)

drawHeader() is similar to statsearchs' drawGameTitle() except that it can support two headers (main title) and four headers (main title + smaller title).

### Bot Commands

An important thing to note from these commands is that they have some similarities with their conventions.  
They usually **tries to prevent errors (increasing user-friendliness), checks for errors, and sends a discord.File object that is the return value of their matching helper function**.

#### vn!help

vn!help is a help command group that displays information about the available commands (vn!help) and optionally the information about a certain command (vn!help {command}). If the *invoke_without_command* argument is True, then the default help command (vn!help) will only be invoked when there is no command specified. Every help command sends an embedded message when called by a Discord user because it looks prettier than plain text.

#### vn!player

vn!player is a command that takes a username as an input, checks its' validity, strips it (to make the command a bit more user-friendly) and lowercases it (for sending a GET request to the players' page, where the link is lowercase), and sends the discord.File object that's returned by the called playerSearch() function.

#### vn!stats

vn!stats is a command similar to vn!player except that it has one additional argument, which is the gamemode chosen (check list of gamemodes using *vn!help stats*) and that it calls statSearch().

#### vn!guild

vn!guild is a command similar to vn!player except that it's for guilds and this command calls the guildSearch() function.

#### vn!lb

vn!lb is a command that gets leaderboard data based on the type of statistic and the page number. The main LB data extraction happens here. To get the link to the leaderboard with the stat given, I have used some dictionaries for conversion of the *stats* as an argument from a user to a link, and it of course does the convention aforementioned that every command does.

### Additional Functions (bot.py)

#### getStatNames(ctx, usage)

This function is commonly associated with the vn!stats and vn!lb command, to display every type of statistic available on the website. The *usage* arg is used to specify the usage of the corresponding command (i.e. vn!stats {gamemode} {player}) which will also be displayed on the embedded message.

#### statErr(ctx, command='stats')

This function is also associated with the vn!stats and vn!lb command, where it is used to send an embedded message whenever a user gave an invalid gamemode as an argument to any of those mentioned commands.

## Final Words

I am very grateful that such amazing CS course exists -- a very easy-to-understand CS course that gives me the fundamental understanding of what programming is and sets me up in a path with many choices; huge thanks to the CS50 team for this course, and I will see you all soon! <3
My personal bot for fetching data from the VenityMC stats website and bundling it into an image.
