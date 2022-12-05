# MusiX
A command line music streamer.

The goal was to make a simple, light-weight and less memory consuming terminal based music streamer.


## Demo for linux
https://user-images.githubusercontent.com/108319876/202860781-28510442-14a4-4d6e-b999-86940c8b5ea3.mp4

## Demo for Windows
https://user-images.githubusercontent.com/108319876/202868200-9b4f2334-2507-49e2-8a14-d8c0fe0d0d1a.mp4

In windows version warnings are frequently shown by VLC on command line. Could'nt find a solution to shut them. Ignore them.

## Controls
- [space] to pause/play
- ctrl+c to quit

## Working:
- User input the song name.
- Using youtube v3 API, search results are produced.
- User selects the song.
- From the JSON data sent by the API, URL and other data like video title and duration are extracted.
- Using `pafy` and `python-vlc` audio is extracted and streamed.
- Using `keyboard` for windows and `pynput` for linux, pause/play control is created. 
- The functionality of these libraries was like keylogger. No matter where you press the key, the function is triggered. So, I added an extra block of code which checks if the current window is same as the window at the time program was started. Only then function is triggered. This is like pause/play control is valid only when window is in focus.
- Another good option was to make a TUI to implement the controls.
- Autoplay is implemented using API's `relatedVideo` query. It sends the video related to current video. In my testing, I experienced the autoplay stuck in an endless loop between two videos. Will try to implement a better autoplay code in future!

### UPDATE:
- If you face any issues or observe high CPU or RAM consumption please let me know. In one of the earlier uploads the CPU consumption was too high because I was printing few lines in every loop. Now, I removed it and print them olny once and optimised the code. The CPU consumption has dropped by almost 50%.
- Changed installation method for linux. Previous installation method was more prone to dependency conflicts and was harmful(ex: packages like ipython3 stopped working). Solved this using `pipx`. Will try to change for windows as well. Till now didn't face any problems with windows.
- The demos were recorded before the above two updates.
