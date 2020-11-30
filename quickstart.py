from __future__ import print_function
import pickle
import os.path
import base64
import time
import random
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

""" ---------------------------------------- """

def create_message(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

""" ---------------------------------------- """

def send_message(service, user_id, message):
    """Send an email message.

    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        message: Message to be sent.

    Returns:
        Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except Exception as error:
        print('An error occurred: %s' % error)

""" ---------------------------------------- """

sbjlist = [
    "red",
    "green",
    "yellow",
    "blue",
    "gray",
    "white",
    "black",
    "pink"
]
msglist = [
    "https://twitter.com/nsfw_funny/status/994893489837170688",
    "Would you rather be a bath or a toilet?",
    "I’ll pay you £50 to shut up.",
    "He’s literally worse than Hitler.",
    "You and my wife could mud-wrestle naked.",
    "Babies aren’t just for Christmas, you know.",
    "I want a piglet. But I’ll get rid of it when it’s a pig.",
    "Anyone interested in a pile of bricks, it’s free on craigslist.",
    "If I had a lightsaber, I would lightly saber you.",
    "Can you show me how to open this banana?",
    "So then I sat on him."
]

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
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

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])

    for i in range(50):
        msg = create_message("me", "niklas.oscarsson@ga.ntig.se", sbjlist[random.randint(0, len(sbjlist)-1)], msglist[random.randint(0, len(msglist)-1)])
        send_message(service, "me",msg)
        time.sleep(1)

if __name__ == '__main__':
    main()

""" ---------------------------------------- """