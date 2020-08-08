# Rocketbook Archiver
This takes PDFs embedded with text from Rocketbook and stores them automatically in Google Drive. Used to solve the Android Rocketbook app's problem where embedded text in PDFs gets deleted while uploading to Google Drive.

## Getting Started
Install python3, pip3.

Install requirements via `pip3 install -r requirements.txt`

Gather credentials as described in the credentials section below.

Then run `python3 uploadNotes.py`

### Credentials
You need to get client_secrets.json from the Google Drive API authentication page from a project created under your email
You need to get credentials.json by enabling the Gmail API for your email

