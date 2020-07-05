import os
import json
import sqlite3
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "D:\Course\client_secret.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)


    request = youtube.subscriptions().list(
        part="snippet",
        channelId="UCqnrUcKVSJX2nSmqJomc5Vw",
        maxResults=50
    )
    response = request.execute()

    # print (json.dumps(response, sort_keys=True, indent=4))
    try:
        #to go through all the pages, one page will show max 50 subscriptions
        nextPageToken = response['nextPageToken']
        while('nextPageToken' in response):
            nextPage = youtube.subscriptions().list(
                part="snippet",
                channelId="UCqnrUcKVSJX2nSmqJomc5Vw",
                maxResults=50,
                pageToken=nextPageToken
            ).execute()
            response['items']=response['items']+nextPage['items']
            if 'nextPageToken' not in nextPage:
                response.pop('nextPageToken', None)
            else:
                nextPageToken = nextPage['nextPageToken']

    except:
        print("Error in nextPageToken")

    # #printing subsribed channel name and id
    # num = 1
    # for it in response['items']:
    #     print(num, '...', it['snippet']['title'], it['snippet']['resourceId']['channelId'])
    #     num = num + 1

    # connection to database
    conn = sqlite3.connect('youtubedata.sqlite')
    cur = conn.cursor()

    # insert into table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Subscriptions (ChannelId TEXT, Name TEXT)''')

    for it in response['items']:
        id = it['snippet']['resourceId']['channelId']
        name = it['snippet']['title']
        # cur.execute('''INSERT INTO Subscriptions(ChannelId, Name)
        #           VALUES (?,?)''', (id, name))
        cur.execute('''INSERT INTO Subscriptions (ChannelId, Name)
                    VALUES ( ?, ? )''', (id, name ))
        conn.commit()





if __name__ == "__main__":
    main()
