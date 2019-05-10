import base64
from apiclient import errors
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import io
import email

#If they change their email formatting, then go down to getAndUploadAttachments and change how you search the snippet 
# (or body if necessary) variable in the first few lines


#To get folder id: Just click get shareable link, and then the long id string is your folder id!

symbolToFolderId = {'apple':"13-pH-CGS5oKSLLorIURKY6BRVcXG2eoN", #CS230/Rocketbook
'bell':"13-pH-CGS5oKSLLorIURKY6BRVcXG2eoN", #CS230/Rocketbook
'clover':"1eq3vyCUtpHHWlYkpU4UvoM1tdj5yCCwm", #CS230
'diamond':"13-pH-CGS5oKSLLorIURKY6BRVcXG2eoN", #CS230/Rocketbook
'star':"1eq3vyCUtpHHWlYkpU4UvoM1tdj5yCCwm", #CS230
'horseshoe':"13-pH-CGS5oKSLLorIURKY6BRVcXG2eoN", #CS230/Rocketbook
'rocket':"1sdM70uGjlN8Ko99EyYqtk4mn3qC9ob8i"} #Random Rocketbook Notes



def getMessageBody(service, user_id, msg_id):
    try:
            message = service.users().messages().get(userId=user_id, id=msg_id, format='raw').execute()
            msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
            mime_msg = email.message_from_bytes(msg_str)
            messageMainType = mime_msg.get_content_maintype()
            if messageMainType == 'multipart':
                    for part in mime_msg.get_payload():
                            if part.get_content_maintype() == 'text':
                                    return part.get_payload()
                    return ""
            elif messageMainType == 'text':
                    return mime_msg.get_payload()
    except errors.HttpError as error:
            print('An error occurred: %s' % error)

def getAndUploadAttachments(service, user_id, msg_id, prefix=""):
    """Get and store attachment from Message with given id.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: ID of Message containing attachment.
    prefix: prefix which is added to the attachment filename on saving
    """
    try:
        # body = getMessageBody(service,user_id,msg_id)
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()
        snippet = message['snippet']
        for key in symbolToFolderId.keys():
            if "#"+key in snippet:
                symbol = key
        for part in message['payload']['parts']:
            if part['filename']:
                if 'data' in part['body']:
                    data=part['body']['data']
                else:
                    att_id=part['body']['attachmentId']
                    att=service.users().messages().attachments().get(userId=user_id, messageId=msg_id,id=att_id).execute()
                    data=att['data']
                file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                path = prefix+part['filename']

                with open(path, 'wb') as f:
                    f.write(file_data)
                
                file_drive = drive.CreateFile({'title':os.path.basename(path) , 'parents':[{
  "kind": "drive#childList",
  "id": symbolToFolderId[symbol]
}]})
                file_drive.SetContentFile(path)
                file_drive.Upload()
                
                os.remove(path)
                msg_labels = {
                    "addLabelIds": [],
                    "removeLabelIds": ["UNREAD"]
                    }
                thread = service.users().messages().modify(userId=user_id, id=msg_id, body=msg_labels).execute()
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

gauth = GoogleAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")

drive = GoogleDrive(gauth)

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
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
        creds = flow.run_local_server()
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('gmail', 'v1', credentials=creds)

user_id =  'me'
label_id_one = 'INBOX'
label_id_two = 'UNREAD'

# Getting all the unread messages from Inbox
# labelIds can be changed accordingly
unread_msgs = service.users().messages().list(userId='me',labelIds=[label_id_one, label_id_two],maxResults=10000).execute()

# We get a dictonary. Now reading values for the key 'messages'
mssg_list = unread_msgs['messages']


for messageDict in mssg_list:
    messageId = messageDict['id']
    message = service.users().messages().get(userId='me',id=messageId).execute()
    payload = message['payload']
    for dictionary in payload['headers']:
        if dictionary['name']=='From' and "notes@email.getrocketbook.com" in dictionary['value']:
            getAndUploadAttachments(service,'me',messageId)

print ("Total unread messages in inbox: ", str(len(mssg_list)))