# these are the two modules that are essential while using the google api do not worry to much about it.
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# the c_secrets.json file is the credintail file which contain the credintials for using the api
# the file shuld have to be in the current working directory

CLIENT_SECRET_FILE = 'c_secrets.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

# reading the credintals from the file and instantialting the youtube api
# this will give a prompt to the user to allow the program to access the user google account
flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
credentials = flow.run_console()
youtube = build('youtube', 'v3', credentials=credentials)


# this is the optional part here i am going to find all the videos at certain time interval
# you can skip this part.
from datetime import datetime
start_time = datetime(year=2020, month=5, day=3).strftime('%Y-%m-%dT%H:%M:%SZ')
end_time = datetime(year=2020, month=5, day=4).strftime('%Y-%m-%dT%H:%M:%SZ')

# here this will execute our request and will be return with all the 
# required information which we have requested
req=youtube.search().list(q='Pakistani vlogs',
                          part='snippet',
                          type='video',
                          publishedAfter=start_time,
                          publishedBefore=end_time,
                          maxResults=50)
res=req.execute()

# in this part we are analyzing the data whcih the youtube api gives us.
# we will parse these informaiton and will find all the youtube videos ids as will the channels ids. 
# which we will combile together to find the exact urls
videos_id=[]
videos=res["items"]
i=0
for video in videos:
    video_id_a=videos[i]
    i=i+1
    video_id_b=video_id_a["id"]
    video_id=video_id_b["videoId"]
    videos_id.append(video_id)
  
  
 channels_id=[]
channels=res["items"]
j=0
for channel in channels:
    channel_id_a=channels[j]
    j+=1
    channel_id_b=channel_id_a["snippet"]
    channel_id=channel_id_b["channelId"]
    channels_id.append(channel_id)
    
 # function for inserting comment on a video
def insert_comment(youtube, channel_id, video_id, text):
    insert_result = youtube.commentThreads().insert(
        part="snippet",
        body=dict(
            snippet=dict(
                channelId=channel_id,
                videoId=video_id,
                topLevelComment=dict(
                    snippet=dict(
                        textOriginal=text)
                )
            )
        )
    ).execute()

    comment = insert_result["snippet"]["topLevelComment"]
    author = comment["snippet"]["authorDisplayName"]
    text = comment["snippet"]["textDisplay"]
    print("Inserted comment for %s: %s" % (author, text))

    
# bulk commenting and handling exceptions  
i=0
import time
try:
    for video in videos_id:
        i+=1
        insert_comment(youtube, channels_id[i],[videos_id[i]], "Is there anyone for friendship. I want to find friends. Kindly visit my channel.")
        time.sleep(3)
except:
    pass
  
  
