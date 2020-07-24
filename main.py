from __future__ import print_function
import pandas as pd 
from datetime import datetime, timedelta   
from matplotlib import pyplot as plt
import telegram
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def time_to_sec(time_str):
    return sum(x * int(t) for x, t in zip([1, 60, 3600], reversed(time_str.split(":"))))

def cronjob():
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    #now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    now = datetime.utcnow()
    minTime = now - timedelta(days = 1) 
    minTime = minTime.isoformat()+ 'Z'
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=minTime,
                                        maxResults=20, singleEvents=True,
                                        orderBy='startTime').execute()
    
    events = events_result.get('items', [])
    f = open("data.csv", "a")
    row="startDate,startTime,endDate,endTime,diff,color,title"+"\n"
    f.write(row)
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = datetime.fromisoformat(event['start'].get('dateTime'))
        startDate = start.date()
        startTime = start.time()
        end = datetime.fromisoformat(event['end'].get('dateTime'))
        endDate = end.date()
        endTime = end.time()
        diff = end - start
        title = event['summary']
        try:
            color = event['colorId']
        except:
            color = '1'
        row = str(startDate)+","+str(startTime)+","+ str(endDate)+","+ str(endTime)+","+ str(diff)+","+ color +","+ title+"\n"
        f.write(row)
        print(startDate,startTime, endDate, endTime, diff, color , title )
    f.close()
