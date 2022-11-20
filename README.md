# MusiX
A command line music streamer



## Demo for linux
https://user-images.githubusercontent.com/108319876/202860781-28510442-14a4-4d6e-b999-86940c8b5ea3.mp4

## Demo fo Windows
https://user-images.githubusercontent.com/108319876/202868200-9b4f2334-2507-49e2-8a14-d8c0fe0d0d1a.mp4

In windows version warnings are frequently shown by VLC on command line. Could'nt find a solution to shut them. Ignore them.

## Controls
- [space] to pause/play
- ctrl+c to quit

## Working:
- User input the song name
- Using youtube v3 API, search results are produced
- User selects the song
- From the JSON data sent by the API, URL and other data like video title and duration are extracted
- Using `pafy` and `python-vlc` audio is extracted and streamed
