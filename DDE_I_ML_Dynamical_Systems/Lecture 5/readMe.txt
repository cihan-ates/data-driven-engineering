
Dear All,

This week we will use a dataset that is not available online. So you need to download
the manufacturing file on your system. If you are using Colab, I recommend you to load it
to your Google Drive, and call it from the GD during the lecture. This is how I set up lecture_3 notebook:

###########################################################
# Loading the data
!pip install -U -q PyDrive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials# Authenticate and create the PyDrive client.
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

downloaded = drive.CreateFile({'id':'<YOUR FILE ID HERE>'}) 
downloaded.GetContentFile('manufacturing.csv')
data = pd.read_csv('manufacturing.csv')
data.head()
#############################################################

You need to upload the file to GD, then share it with a link. In the link, you will have the ID of the file,
which you need to write under <YOUR FILE ID HERE> above.

Alternatively, you can upload it from your local pc. To do so, you need to un-do the commenting out
for the following lines:

###########################################################

# Loading the data

#Local drive:
#from google.colab import files
#uploaded = files.upload()
#data = pd.read_csv('manufacturing.csv')
#data.head()
###########################################################

and comment out the following lines:

###########################################################
# Loading the data
!pip install -U -q PyDrive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials# Authenticate and create the PyDrive client.
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

downloaded = drive.CreateFile({'id':'1mQZTB5gEkal_qH0TiivXAJY082Wclfbo'}) 
downloaded.GetContentFile('manufacturing.csv')
data = pd.read_csv('manufacturing.csv')
data.head()
###########################################################

Please do the modifications before the lecture!

---------------- C. Ates ----------------