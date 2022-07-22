# Create a function for retrieving a players' general stats

import searchlib as search

# API version
def api_player(name):
    player_text = search.webText(f"{name}").json()
    

def playerSearch(playerText):
    # Get players' statistics
    playerStats = playerText.select('td[class=col-xs-9]')

    # Load template
    template, drawTemplate = search.copyTemplate()

    # Variables for text positioning and coloring
    SIZE1, SIZE2 = 36, 48
    CENTER, HEADING = (template.width / 2, 100)
    MAINHEADCOLOR, MAINSTATCOLOR = ("white", "yellow")

    # Draw players' name
    name_height = search.drawName(playerText.select('td[class=col-xs-9] > span'), drawTemplate, CENTER, HEADING)
    
    # Draw players' head -- determine its' X and Y coordinates
    X1 = CENTER - 105
    Y1 = HEADING + name_height + 30
    search.drawHead(drawTemplate, template, playerText, X1, Y1, X1 + 210, Y1 + 210)

    # Draw players' activity status on server (on/offline)
    statusdata = ["Status:", '', '']
    statuscolor = [MAINHEADCOLOR, MAINSTATCOLOR]

    # If player is online, text = [ONLINE]
    if playerStats[8].get_text(strip=True) == "Online":
        statusdata[1] = "[ONLINE]"
        statuscolor.insert(1, (8, 156, 0))

    # If player is offline, text = [OFFLINE] Last seen ...
    else:
        statusdata[1], statusdata[2] = ("[OFFLINE]", 'Last seen ' + playerStats[8].get_text(strip=True))
        statuscolor.insert(1, (255, 0, 0))
    
    # Player status text positioning and size
    stsizes = [SIZE1, SIZE2, 24]
    status_Y_pos = HEADING + name_height + 260

    # Draw player status text with for loop
    for i in range(len(stsizes)):
        w, h = search.font(stsizes[i]).getsize(statusdata[i])
        drawTemplate.text((search.midPos(w), status_Y_pos), statusdata[i], fill=statuscolor[i], font=search.font(stsizes[i]))
        status_Y_pos += h + 5

    # Draw players' other stats
    statHeaders = ("First Join:", "Playtime:", "ELO:", "Coins:")
    stats = [playerStats[7].get_text(strip=True)[:-13]] + [playerStats[i].get_text(strip=True) for i in [3, 2, 4]]
    startingY = status_Y_pos + 50
    settings = ["left", "right"]

    # Draw two stats at a time, left and right
    for i in [0, 2]:
        for j in range(2):
            shH = search.font(SIZE1).getsize(statHeaders[i + j])[1]
            search.drawStat(drawTemplate, settings[j], startingY, statHeaders[i + j], SIZE1)
            search.drawStat(drawTemplate, settings[j], startingY + shH + 5, stats[i + j], SIZE2, "yellow")
        startingY += shH + search.font(SIZE2).getsize(stats[i + j])[1] + 100
    
    # Draw additional text for "first joined" stat
    fj2 = playerStats[7].get_text(strip=True)[12:]
    fj2w = search.font(28).getsize(fj2)[0]
    drawTemplate.text((search.midPos(fj2w, 4), status_Y_pos + 130), fj2, fill=MAINSTATCOLOR, font=search.font(28))

    # Draw players' level
    search.drawLevel(playerStats, drawTemplate, CENTER, MHC=MAINHEADCOLOR, MSC=MAINSTATCOLOR)

    # Return the name and directory of the created image
    return search.byte(template)
