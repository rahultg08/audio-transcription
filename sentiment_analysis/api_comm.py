import requests                                             # making use of API
from api_key import API_KEY
import json
import time

# upload the local audio files   (Not needed now!)
# upload_endpoint = 'https://api.assemblyai.com/v2/upload'
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"

headers_auth_only = {'authorization': API_KEY}

headers = {'authorization': API_KEY, "content-type": "application/json"}

CHUNK_SIZE = 5_242_880                       # 5MB

# upload not needed as we work on urls
# def upload(filename):
#     def read_file(filename, chunk_size=5242880):
#         with open(filename, 'rb') as _file:
#             while True:
#                 data = _file.read(chunk_size)
#                 if not data:
#                     break
#                 yield data

#     upload_response = requests.post(upload_endpoint,
#                             headers=headers_auth_only,
#                             data=read_file(filename))

#     audio_url = upload_response.json()['upload_url']        #contains the url of the uploaded audio file
#     # print(upload_response.json())
#     return audio_url

# transcription of the uploaded audio file
def transcribe(audio_url, sentiment_analysis):
    transcript_request = { "audio_url": audio_url, "sentiment_analysis":sentiment_analysis }
    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers)
    # print(transcript_response.json())
    job_id = transcript_response.json()['id']
    return job_id


   # transcript_id = transcribe(audio_url)
 
   # print(transcript_id)

# poll to notify when transcription is done
def poll(transcript_id):
    polling_endpoint = transcript_endpoint + '/' + transcript_id
    polling_response = requests.get(polling_endpoint, headers = headers)                            # polling if the job is done
    return polling_response.json() 

def get_transcription_result_url(audio_url, sentiment_analysis):                                    # checking the status regularly
    transcript_id = transcribe(audio_url, sentiment_analysis)
    while True:
        data = poll(transcript_id)
        if data['status'] == 'completed':
            return data, None
        elif data['status'] == 'error':
            return data, data['error']
        print("Waiting for 30 secs...")
        time.sleep(30)

# save the transcribed data
def save_transcript(audio_url, title, sentiment_analysis = False):
    data, error = get_transcription_result_url(audio_url, sentiment_analysis)
    if data:
        outputtxt = title+".txt"
        with open(outputtxt, "w") as f:
            f.write(data['text'])

        if sentiment_analysis:                                                  # if sentiment analysis has to be done
            filename = title + "_sentiment.json"
            with open(filename, "w") as f:
                sentiments = data['sentiment_analysis_results']
                json.dump(sentiments, f, indent=4)
        print("Audio transcripted & sentiment analysed! Saved in the directory")
        return True
    else:
        print("Error!", error)
        return False




