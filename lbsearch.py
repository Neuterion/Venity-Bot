# Create functions for retrieving leaderboard data

import searchlib as search


def drawLB(lbtext, page, nameLB, statLB, mode=''):
    # Load template
    template, drawTemplate = search.copyTemplate()

    # General font size
    SIZE = 48

    # Center = center text pos, heading sets the mark where all the text will start top to bottom
    CENTER, HEADING = template.width / 2, 300

    # Generate list of numbers for each rank
    # page * 10 - 8 + len(statLB) is the same as page * 10 - 9 + len(statLB) + 1
    RANK = [str(i) + '.' for i in range(page * 10 - 9, page * 10 - 8 + len(statLB))]

    # Web-scrape the leaderboard headers and get the texts' width
    lbHeader = [lbtext.select('thead > tr > td')[i].get_text() for i in [0, 2, 3]]
    lbhW = [search.font(SIZE).getsize(i)[0] for i in lbHeader]

    # Draw the headers
    drawTemplate.text((CENTER / 3 - lbhW[0] / 2, HEADING - 75), lbHeader[0], fill="white", font=search.font(SIZE))
    drawTemplate.text((CENTER - lbhW[1] / 2, HEADING - 75), lbHeader[1], fill="white", font=search.font(SIZE))
    drawTemplate.text((CENTER * 2 - CENTER / 3 - lbhW[2] / 2, HEADING - 75), lbHeader[2], fill="white", font=search.font(SIZE))

    # List of gamemode titles and modes
    gm = ("Solo", "Doubles", "3v3v3v3", "4v4v4v4")
    games = {
        "sw": ("Sky", "Wars", "yellow", "white"),
        "bw": ("Bed", "Wars", "white", "red"),
        "tb": ("The", "Bridge", "red", "blue"),
        "duels": ("Duels", "", "orange", "orange"),
        "tntrun": ("TNT", "Run", "red", "white")
    }
    genStats = {
        "guild": ("Guild", "Level", "white", "blue"),
        "elo": ("ELO", '', "white", "white"),
        "playtime": ("Play", "time", "white", "green"),
        "level": ("Level", '', "white", "white")
    }

    # Draw LB header
    if mode[:2] in [*games]:
        drawHeader(drawTemplate, games[mode[:2]][2], games[mode[:2]][3], games[mode[:2]][0], games[mode[:2]][1], "Mode: ",
                   gm[int(mode[2]) - 1])
    elif mode in [*games]:
        drawHeader(drawTemplate, games[mode][2], games[mode][3], games[mode][0], games[mode][1], "Mode: ", "Solo")
    else:
        drawHeader(drawTemplate, genStats[mode][2], genStats[mode][3], genStats[mode][0], genStats[mode][1])

    # Draw main leaderboard data
    for i in range(len(nameLB)):
        rankW = search.font(SIZE).getsize(RANK[i])[0]
        drawTemplate.text((CENTER / 3 - rankW / 2, HEADING), RANK[i], fill="white", font=search.font(SIZE))

        statW = search.font(SIZE).getsize(statLB[i])[0]
        drawTemplate.text((CENTER * 2 - CENTER / 3 - statW / 2, HEADING), statLB[i], fill="white", font=search.font(SIZE))

        nameHeight = search.drawName(nameLB[i], drawTemplate, CENTER, HEADING)

        HEADING += nameHeight + 30

    # Return the name and directory of the created image
    return search.byte(template)


def drawHeader(draw, col1, col2, *headers):
    # Generate list of fonts and font sizes to use them on generating a list of the sizes of the header texts
    fonts, sizes = [search.bFont, search.bFont, search.font, search.font], [72, 72, 36, 36]
    headerWH = [f(size).getsize(i) for f, size, i in zip(fonts, sizes, headers)]

    # Draw headers, the options are 2 or 4
    draw.text((search.midPos(headerWH[0][0] + headerWH[1][0]), 50), headers[0], fill=col1, font=search.bFont(72))
    draw.text((search.midPos(headerWH[0][0] + headerWH[1][0]) + headerWH[0][0], 50), headers[1], fill=col2, font=search.bFont(72))
    if len(headers) == 4:
        draw.text((search.midPos(headerWH[2][0] + headerWH[3][0]), 55 + headerWH[0][1]),
                  headers[2], fill=col2, font=search.font(36))
        draw.text((search.midPos(headerWH[2][0] + headerWH[3][0]) + headerWH[2][0],
                  55 + headerWH[0][1]), headers[3], fill=col1, font=search.font(36))
