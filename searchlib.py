import requests
import bs4
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageColor
from io import BytesIO
from discord import File


# Returns a font object
def font(size): return ImageFont.truetype('fonts/minecraft.otf', size)


# Returns a bold font object
def bFont(size): return ImageFont.truetype('fonts/minecraftbold.otf', size)


# Returns a BytesIO object of a players' head skin image
def headSkin(src): return BytesIO(requests.get(src).content)


# Returns all HTML text from a certain page
def webText(route):
    try:
      req = requests.get(f"https://player.venitymc.com/{route}", timeout=5)
    except:
      return bs4.BeautifulSoup('')
    return bs4.BeautifulSoup(req.text, "html.parser")


# Returns the X coordinates to where some text should be placed
# The default is the middle which is why the default value of div is 2, to divide the img width in half
def midPos(width, div=2): return 1920 / div - width / 2


# Check if a string has a digit in it
def isdigit(text):
    if True in [char.isdigit() for char in text]:
        return True
    return False


# Returns a list with the selected element all removed from it
def delete(lst, element):
    while element in lst:
        lst.remove(element)
    return lst


# Converts a PIL image object into a BytesIO object which Discord supports when sending a file from a bot
def byte(template):
    arr = BytesIO()
    template.save(arr, format='PNG')
    arr.seek(0)

    return File(arr, filename="player.png")


class Template:
    def __init__(self):
        self.file = Image.open('bgtemplates/playerbg.png').filter(ImageFilter.GaussianBlur(7)).copy()
        self.draw = ImageDraw.Draw(self.file)

    def save(self, username: str):
        arr = BytesIO()
        self.file.save(arr, format='PNG')
        arr.seek(0)

        return File(arr, filename=f"{username.replace(' ', '_')}.png")


# Creates a new PIL image from copying the provided templates
def copyTemplate():
    template = Image.open('bgtemplates/playerbg.png').filter(ImageFilter.GaussianBlur(7)).copy()
    # Create ImageDraw object for the template, to draw text/shapes on
    draw = ImageDraw.Draw(template)

    return (template, draw)


# Draws a players'/guilds' name on a PIL image
def drawName(nameData, draw, W, Y, drawguild=True):
    # Delete list of seperated player name HTML tags from the newline symbol (dk why it happens)
    nameData = delete(nameData, '\n')
    taglist, col, text = [], [], []

    # Check if the first part of the name belongs to a player or guild
    if 'span' not in str(nameData[0]):
        col.append("white")
        text.append(str(nameData[0]).strip())
    else:
        # It must be a players' name, so now turn it into a BS4 object
        nameData[0] = bs4.BeautifulSoup(" ".join(str(nameData[0]).split()), 'html.parser')

        # Extracting all tags from the nested tags and adding them to the col & text list
        while nameData[0].span != None:
            nameData[0] = nameData[0].span
            taglist.append(nameData[0])
        for i in range(len(taglist) - 1):
            taglist[i] = bs4.BeautifulSoup(str(taglist[i]).replace(str(taglist[i + 1]), ''), 'html.parser')
        for i in range(len(taglist)):
            col.append(ImageColgor.getcolor(str(taglist[i])[19:23], 'RGB'))
            text.append(taglist[i].get_text(strip=True))

    if drawguild == True:
        # Check if player has a guild / get a guilds' tag and append it to the col and text list
        if len(nameData) == 1 or (len(nameData) > 1 and '[' not in nameData[1].get_text()):
            text[0] = text[0].strip()
            gcolor = 'white'
            gtext = ''
        else:
            gcolor = ImageColor.getcolor(str(nameData[1])[19:23], 'RGB')
            gtext = ' ' + nameData[1].get_text()

        # Append the guild text & color, depends on whether the player is in a guild
        col.append(gcolor)
        text.append(gtext)

    # Get the sizes of all the texts and the starting position of writing the whole text
    textwh = [font(48).getsize(i) for i in text]
    startingtxtpos = W - sum([i[0] for i in textwh]) / 2

    # Draw it by for loop
    for i in range(len(text)):
        draw.text((startingtxtpos, Y), text[i], fill=col[i], font=font(48))
        startingtxtpos += textwh[i][0]

    # Return one of the texts' height as a benchmark for the new Y position of some text that's going to be drawn below the name
    return textwh[0][1]


# Draw a players'/guilds' level
def drawLevel(webText, draw, W, gap=100, MHC="white", MSC="yellow", isplayer=True):
    # Check if level belongs to a player or guild
    if isplayer == False:
        lvlXP = str(webText[4].get_text(strip=True))
    else:
        lvlXP = str(webText[1].get_text(strip=True))

    # Insert text about players'/guilds' level
    levelHead = "Level / EXP:"
    levelHeadWH = font(36).getsize(levelHead)

    # Get the level and its' size in text
    level = lvlXP[:(lvlXP.find('/') - 1)]
    levelWH = font(36).getsize(level)

    # Get the amount of XP the player has on that level and the amount of XP needed to reach the next level
    xp1 = lvlXP[lvlXP.find('(') + 1:lvlXP.rfind('/')]
    xp2 = lvlXP[lvlXP.rfind('/') + 1:lvlXP.find(')')]

    # Determine the starting position of the texts and the bars' size
    barWidth, barHeight = 380, 30
    startYpos = 1080 - (levelHeadWH[1] + levelWH[1] + barHeight + gap)

    # Draw level header and players' level
    draw.text((midPos(levelHeadWH[0]), startYpos), levelHead, fill=MHC, font=font(36))
    draw.text((midPos(levelWH[0]), startYpos + levelHeadWH[1] + 5), level, fill=MSC, font=font(36))

    # Draw bar
    draw.rectangle((midPos(barWidth + 20), startYpos + levelHeadWH[1] + levelWH[1] + 10, midPos(
                   barWidth + 20) + barWidth + 20, startYpos + levelHeadWH[1] + levelWH[1] + barHeight + 20), fill="black", outline="black")
    draw.rectangle((midPos(barWidth), startYpos + levelHeadWH[1] + levelWH[1] + 20, midPos(barWidth) + barWidth * float(
                   xp1.replace(',', '')) / float(xp2.replace(',', '')), startYpos + levelHeadWH[1] + levelWH[1] + barHeight + 10), fill="yellow")

    # Draw XP text
    draw.text((midPos(barWidth + 20) - font(36).getsize(xp1)[0] - 5, startYpos +
              levelHeadWH[1] + levelWH[1] + 15), xp1, fill=MSC, font=font(36))
    draw.text((W + barWidth / 2 + 25, startYpos + levelHeadWH[1] + levelWH[1] + 15), xp2, fill=MSC, font=font(36))


# Draw a players' head
def drawHead(draw, template, webText, X1, Y1, X2, Y2):
    # Draw a frame around the head image
    draw.rectangle((X1, Y1, X2, Y2), fill="black", outline="black")
    # Get the head image and paste it in the middle of the frame
    try:
        template.paste(Image.open(headSkin(webText.find('img').attrs['src'])), (int(X1) + 10, Y1 + 10))
    except:
        pass
    # Draw an outline around the image
    draw.rectangle((X1 + 10, Y1 + 10, X2 - 10, Y2 - 10), outline="white")


# Draw some sort of statistic
def drawStat(draw, relPos, Ypos, text, size, col="white"):
    # Get width of stat text
    textwidth = font(size).getsize(text)[0]

    # Determine the position of the text on the image based on input
    if relPos == "left":
        relPos = 1920 / 4 - textwidth / 2
    else:
        relPos = 1920 * 0.75 - textwidth / 2

    # Draw the text
    draw.text((relPos, Ypos), text, fill=col, font=font(size))
