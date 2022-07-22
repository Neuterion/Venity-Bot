# Create functions for retrieving a players' certain gamemode stats

import searchlib as search


def statSearch(game, mode, playerText):
    # Load template and MC font
    template, drawTemplate = search.copyTemplate()
    
    # Create variable for center text postioning
    CENTER = template.width / 2
    SIZE1, SIZE2 = 36, 48

    # Lists of web-scraped gamemode stats corresponding to the chosen gamemode
    mode = int(mode) - 1
    modes = ("Solo", "Doubles", "3v3v3v3", "4v4v4v4")
    bw123 = playerText.select('div[id=bedwars] > table > td')
    gmStats = {
        "bw": [[i.get_text() for i in bw123[15:21]], [i.get_text() for i in bw123[8:14]],
               [i.get_text() for i in bw123[1:7]], [i.get_text() for i in playerText.select('div[id=bedwars] > table > tr > td')[8:14]]],
        "sw": [[i.get_text() for i in playerText.select('div[id=skywars] > table > td')[1:]],
               [i.get_text() for i in playerText.select('div[id=skywars] > table > tr > td')[6:]]],
        "tb": [[i.get_text() for i in playerText.select('div[id=thebridge] > table > td')[1:]],
               [i.get_text() for i in playerText.select('div[id=thebridge] > table > tr > td')[7:]]],
        "duels": [[i.get_text() for i in playerText.select('div[id=duels] > table > td')[1:]]],
        "tntrun": [[i.get_text() for i in playerText.select('div[id=tntrun] > table > td')[1:]]]
    }
    gmHeads = {
        "bw": ["Wins:", "Matches:", "Final Kills:", "Total Kills:", "Beds Broken:", "KDR:"],
        "sw": ["Wins:", "Matches:", "Kills:", "KDR:"],
        "tb": ["Wins:", "Matches:", "Kills:", "Goals:", "KDR:"],
        "duels": ["Wins:", "Matches:", "KDR:"],
        "tntrun": ["Wins:", "Matches:"]
    }

    # Checking for valid gamemode
    if game not in [*gmStats]:
        return False

    # Draw gamemode title and get its' total height
    TITLEHEADING = drawGameTitle(game, modes[mode], drawTemplate)
    
    # Draw players' head by determining its' X and Y coordinates
    frameXpos, frameYpos = CENTER - 105, TITLEHEADING + 30
    search.drawHead(drawTemplate, template, playerText, frameXpos, frameYpos, frameXpos + 210, frameYpos + 210)
    
    # Draw players' name by entering the X, Y coordinates
    search.drawName(playerText.select('td[class=col-xs-9] > span'), drawTemplate, CENTER, frameYpos + 220)

    # Draw players' gamemode stats by for loop
    textpos = ["left", "right"]
    startingYpos = frameYpos + 300
    # Draw two stats at once, left and right, which is the reason for a nested for loop
    for i in range(0, len(gmHeads[game]), 2):
        for j in range(2):
            if i + j < len(gmHeads[game]):
                statHeadH = search.font(SIZE1).getsize(gmHeads[game][i + j])[1]
                search.drawStat(drawTemplate, textpos[j], startingYpos, gmHeads[game][i + j], SIZE1)
                search.drawStat(drawTemplate, textpos[j], startingYpos + statHeadH + 5, gmStats[game][mode][i + j], SIZE2, "yellow")
        startingYpos += 150

    # Draw players' level with X, Y coordinates
    search.drawLevel(playerText.select('td[class=col-xs-9]'), drawTemplate, CENTER)

    # Return the name and directory of the created image
    return search.byte(template)


def drawGameTitle(game: str, mode: str, drawTemplate):
    # Heading is for the position of the first text
    HEADING = 50
    SIZE1 = 36

    # Determine gamemode title for image
    if game == "duels":
        header1, header2 = "Duels", ''
        header1col, header2col = "yellow", "white"
    elif game == "bw":
        header1, header2 = "Bed", "Wars"
        header1col, header2col = "red", "white"
    elif game == "sw":
        header1, header2 = "Sky", "Wars"
        header1col, header2col = "white", "yellow"
    elif game == "tntrun":
        header1, header2 = "TNT", "Run"
        header1col, header2col = "red", "white"
    elif game == "tb":
        header1, header2 = "The", "Bridge"
        header1col, header2col = "red", "blue"

    # Get the width and height of the gamemodes' titles and draw them
    header1wh = search.bFont(72).getsize(header1)
    header2wh = search.bFont(72).getsize(header2)
    drawTemplate.text((search.midPos(header1wh[0] + header2wh[0]), HEADING), header1, fill=header1col, font=search.bFont(72))
    drawTemplate.text((search.midPos(header1wh[0] + header2wh[0]) + header1wh[0],
                       HEADING), header2, fill=header2col, font=search.bFont(72))

    # Get the width and height of the gamemodes' mode text and draw it
    modetitle_wh = search.font(SIZE1).getsize("Mode: ")
    modeW = search.font(SIZE1).getsize(mode)[0]
    drawTemplate.text((search.midPos(modetitle_wh[0] + modeW), HEADING + header1wh[1] + 5),
                      "Mode: ", fill=header2col, font=search.font(SIZE1))
    drawTemplate.text((search.midPos(modetitle_wh[0] + modeW) + modetitle_wh[0], HEADING + header1wh[1] + 5),
                      mode, fill=header1col, font=search.font(SIZE1))

    # Return new heading coordinate by adding the titles' height
    return HEADING + header1wh[1] + modetitle_wh[1] + 5
