
# Table of Contents

1.  [Overview](#org2d0cc27)
2.  [Installation](#orgf5b5fca)
    1.  [Docker Install](#org799d599)
    2.  [Installation On Unraid](#org7baa9c1)
3.  [Commands](#orgacd88a9)



<a id="org2d0cc27"></a>

# Overview

This is a simple Discord music bot built utilizing Python, Docker, and yt-dlp. I made this bot to self host it on my Unraid server, but you can host it without Unraid as well as long as you have Docker.


<a id="orgf5b5fca"></a>

# Installation


<a id="org799d599"></a>

## Docker Install

1.  Pull the Docker image:
    
        docker pull sticio/discord-music-bot

2.  Run the bot with your token:
    
        docker run -e DISCORD_BOT_TOKEN="your-token-here" sticio/discord-music-bot


<a id="org7baa9c1"></a>

## Installation On Unraid

1.  Open the ****Unraid Web UI****.
2.  Go to the ****Docker**** tab and click ****Add Container****.
3.  Set the ****Repository**** to: sticio/discord-music-bot
4.  Under ****Environment Variables****, add:
5.  ****Key****: \`DISCORD_BOT_TOKEN`
6.  ****Value****: \`your-bot-token-here\`
7.  Click ****Apply**** and start the container.


<a id="orgacd88a9"></a>

# Commands

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Command</th>
<th scope="col" class="org-left">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td class="org-left">!play [song]</td>
<td class="org-left">Plays a song from YouTube</td>
</tr>

<tr>
<td class="org-left">!skip</td>
<td class="org-left">Skips the current song</td>
</tr>

<tr>
<td class="org-left">!queue</td>
<td class="org-left">Shows the song queue</td>
</tr>

<tr>
<td class="org-left">!loop</td>
<td class="org-left">Toggles looping</td>
</tr>

<tr>
<td class="org-left">!join</td>
<td class="org-left">Joins voice channel</td>
</tr>

<tr>
<td class="org-left">!leave</td>
<td class="org-left">Disconnects from the voice channel</td>
</tr>
</tbody>
</table>

