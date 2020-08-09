# Rocketbook Archiver
This takes PDFs embedded with text from Rocketbook and stores them automatically in Google Drive. Used to solve the Android Rocketbook app's problem where embedded text in PDFs gets deleted while uploading to Google Drive.


### Prerequisites

python3, pip3, required packages (can be installed via `pip3 install -r requirements.txt`)

## Getting Started

Gather credentials as described in the credentials section below.

Edit the symbol-folder mapping in uploadNotes.py as described in the file.

Then run `python3 uploadNotes.py`

### Credentials
You need to get client_secrets.json from the Google Drive API authentication page from a project created under your email
You need to get credentials.json by enabling the Gmail API for your email

## Authors

* **Suchir Bhatt**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
