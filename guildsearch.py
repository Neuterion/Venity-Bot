# Create function for retrieving a guilds' statistics

import searchlib as search
import requests, discord, json


def get_guild_members(ctx, name):
    member_list = requests.get(f"https://player.venitymc.com/api/v1/guild/{name}").json()
    
    if len(member_list) == 0:
        return None
        
    print(member_list)
    print(type(json.dumps(member_list["officers"])))
    
    name = member_list["guild"]
    leader = member_list["leader"]
    officers = ", ".join(member_list["officers"].sort())
    members = ", ".join(member_list["members"].sort())
    
    embed = discord.Embed(title=f"{name} Members", color=ctx.author.color)
    embed.add_field(name="Leader", value=f"{leader}")
    embed.add_field(name="Officers", value=f"{officers}")
    embed.add_field(name="Members", value=f"{members}")
    
    return embed


def guildSearch(guildpage):
    # Retrieve all data about guild
    guildText = guildpage.select('td.col-xs-9')

    # Load template
    template, drawTemplate = search.copyTemplate()

    # Variables for text positioning and coloring
    SIZE1, SIZE2 = 36, 48
    CENTER, HEADING = (template.width / 2, 100)
    MAINHEADCOLOR, MAINSTATCOLOR = ("white", "yellow")

    gNametagH = search.drawName([guildText[0].get_text()] +
                                guildpage.select('td[class=col-xs-9] > span'), drawTemplate, CENTER, HEADING)

    # Get link of guild leader
    leader_link = guildpage.select('td[class=col-xs-9] > a')[0].attrs['href']
    leaderData = search.webText(leader_link[1:])

    # Draw header for guild leader
    guildLeaderHead = "Leader:"
    glhWH = search.font(SIZE1).getsize(guildLeaderHead)
    drawTemplate.text((search.midPos(glhWH[0]), HEADING + gNametagH + 50),
                      guildLeaderHead, fill=MAINHEADCOLOR, font=search.font(SIZE1))

    # Draw leaders' head
    X1 = CENTER - 105
    Y1 = HEADING + gNametagH + glhWH[1] + 60
    search.drawHead(drawTemplate, template, leaderData, X1, Y1, X1 + 210, Y1 + 210)

    # Draw leaders' name and retrieve the texts' height
    nameHeight = search.drawName(leaderData.select('td[class=col-xs-9] > span'),
                                 drawTemplate, CENTER, HEADING + gNametagH + glhWH[1] + 280, drawguild=False)

    # Draw guild stats
    guildStatHeaders, statPlacement = ("Members:", "Created At:"), ("left", "right")
    guildstats = [guildText[2].get_text(strip=True), str(guildText[5].get_text(strip=True))[:-13]]
    startingY = HEADING + gNametagH + nameHeight + 400

    # With for loop
    for i in range(len(guildStatHeaders)):
        statheader_wh = search.font(SIZE1).getsize(guildStatHeaders[i])
        search.drawStat(drawTemplate, statPlacement[i], startingY, guildStatHeaders[i], size=SIZE1)
        search.drawStat(drawTemplate, statPlacement[i], startingY + statheader_wh[1] + 5, guildstats[i], size=SIZE2, col="yellow")
     
    # Draw guild level
    search.drawLevel(guildText, drawTemplate, CENTER, 150, MAINHEADCOLOR, MAINSTATCOLOR, isplayer=False)

    # Return the name and directory of the created image
    return search.byte(template)
