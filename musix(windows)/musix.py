import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
import pafy
import vlc
from pyfiglet import Figlet
from PyInquirer import prompt
import sys
import keyboard
import ctypes
import time


# Suppress traceback errors #
# Ctrl + C to quit #
class DevNull:
    def write(self, msg):
        pass
sys.stderr = DevNull()


## Function to get current window in focus ##
def getWindow():
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
    buff = ctypes.create_unicode_buffer(length + 1)
    ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
    return buff.value # buff.value is the title of the window, hwnd is the window handle
#

#Store terminal used when program started first time
appInUse=''


### Command function ###
def musix():

    # Get api-key #
    load_dotenv()
    api_key=os.environ.get('api_key')

    # Build Youtube engine #
    youtube=build('youtube','v3',developerKey=api_key)

    def autoplay():
        questions=[
            {
                'type': 'confirm',
                'message': 'Do you want to have autoplay?',
                'name': 'autoplay',
                'default': True,
            },
        ]

        res = prompt(questions)
        return res['autoplay']
    #



    def songQuery():
        questions=[
            {
                'type': 'input',
                'name': 'song',
                'message': 'Search:',
            }
        ]
        query=prompt(questions)
        return query   #{song:song name} is returned
    #

    def getDuration(video_id):
        #Get video Length using another API call
        list_video_byid = youtube.videos().list(id = video_id,part = "contentDetails",).execute()
        isoduration=list_video_byid['items'][0]['contentDetails']['duration']

        duration="";

        i=0;
        while(i<len(isoduration)):
            if(isoduration[i]>='A'):
                if(isoduration[i]=='P' or isoduration[i]=='T' or isoduration[i]=='S'): pass;
                else: duration+=':';
            else:
                duration+=isoduration[i];
            i+=1;
        #
        return duration
    #

    def search(query):
        #Get results
        request=youtube.search().list(part='id,snippet',q=query,maxResults=5,type='video')
        #Get JSON Data
        response=request.execute()

        #Fetch results
        results=[]
        for item in response['items']:
            video_title=item['snippet']['title']
            video_id = item["id"]["videoId"]

            video_song_data = {
                'name': video_title + ' - (' + getDuration(video_id) + ')',
                'value': f'https://www.youtube.com/watch?v={video_id}',
            }

            results.append(video_song_data)
        #

        return results
    #

    def listResults(results):
        questions=[
            {
                'type': 'list',
                'name': 'searchResult',
                'message': 'Search Results:',
                'choices': results,
            },
        ]

        choice = prompt(questions)
        return choice   #{searchResult:url} is returned
    #


    def streamSong(songURL):

        def pausePlayMusic():
            currentApp=getWindow();
            if(currentApp==appInUse):
                if(player.is_playing()):
                    player.pause();
                else:
                    player.play();
            else:
                pass
        #

        url = songURL
        video = pafy.new(url)
        best = video.getbestaudio()
        playurl = best.url

        ## Creating our player ##
        Instance = vlc.Instance()
        #Create player
        player = Instance.media_player_new()
        #Create media out of the url
        Media = Instance.media_new(playurl)
        Media.get_mrl()
        #Bind player and media
        player.set_media(Media)
        player.play()

        startHotkey=False;
        loading=False;
        playing=False;
        pause=False;

        states=["State.Playing","State.Opening","State.Paused","State.NothingSpecial","State.Buffering"]

        while str(player.get_state()) in states:
            if str(player.get_state())=="State.Opening" and loading==False:
                print("Status: Loading       ",end="\r")
                loading=True;

            if str(player.get_state())=="State.Playing" and playing==False:
                if(startHotkey==False):
                    keyboard.add_hotkey('space', lambda: pausePlayMusic())
                    startHotkey=True;
                #
                print("Status: Playing       ",end="\r")
                playing=True; loading=False; pause=False;

            if str(player.get_state())=="State.Paused" and pause==False:
                print("Status: Paused        ",end="\r")
                pause=True; loading=False; playing=False;
        #

        print("")
        print("Status: Finish")

        keyboard.unhook_all_hotkeys() # remove all hotkeys

        player.stop()   
    #


    def confirm_continue():
        questions=[
            {
                'type': 'confirm',
                'message': 'Do you want to continue?',
                'name': 'continue',
                'default': True,
            },
        ]

        res = prompt(questions)
        return not res['continue']
    #


    def relatedSong(curURL):
        choiceVideoID=curURL[32:]
        relatedVideo = youtube.search().list(part='id,snippet',relatedToVideoId=choiceVideoID,maxResults=2,type='video').execute()
        # print(relatedVideo);
        relatedVideoId=relatedVideo['items'][0]['id']['videoId']
        relatedvideo_title=relatedVideo['items'][0]['snippet']['title'] + ' - (' + getDuration(relatedVideoId) + ')'
        url=f'https://www.youtube.com/watch?v={relatedVideoId}'
        return (relatedvideo_title,url)
    #


    ##### Main ######
    def main1():

        query=songQuery();

        results=search(query['song']);

        choice=listResults(results);

        streamSong(choice['searchResult']);
        
        return confirm_continue()
    #

    
    def main2():

        query=songQuery();

        results=search(query['song']);

        choice=listResults(results);
        curURL=choice['searchResult']

        streamSong(curURL);

        while True:
            nextsong=relatedSong(curURL);
            print("Now Playing: " + nextsong[0]);
            
            time.sleep(3);

            streamSong(nextsong[1]);
            curURL=nextsong[1]
        #
    #



    # Prints Banner #
    figlet=Figlet(font='big')
    print(figlet.renderText('MusiX'))

    #when program starts, first finds which terminal is being used
    appInUse=getWindow()

    autoplayOption=autoplay();

    if(autoplayOption):
        main2();
    else:
        while True:
            userExit=main1();
            if userExit:
                break;
        #
    print("Thanks for using!")
#