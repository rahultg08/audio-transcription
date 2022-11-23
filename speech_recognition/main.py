import sys              #for taking input from the terminal
from api_comm import *
filename = sys.argv[1]                      # terminal input


# Working
audio_url = upload(filename)
save_transcript(audio_url, filename)