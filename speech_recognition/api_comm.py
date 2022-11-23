import requests         #making use of API
from api_key import API_KEY

import time

# upload the local audio files
upload_endpoint = 'https://api.assemblyai.com/v2/upload'
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"


headers = {'authorization': API_KEY}

def upload(filename):
    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    upload_response = requests.post(upload_endpoint,
                            headers=headers,
                            data=read_file(filename))

    audio_url = upload_response.json()['upload_url']        #contains the url of the uploaded audio file
    # print(upload_response.json())
    return audio_url

# transcription of the uploaded audio file
def transcribe(audio_url):
    transcript_request = { "audio_url": audio_url }
    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers)
    # print(transcript_response.json())
    job_id = transcript_response.json()['id']
    return job_id


   # transcript_id = transcribe(audio_url)
 
   # print(transcript_id)

# poll to notify when transcription is done
def poll(transcript_id):
    polling_endpoint = transcript_endpoint + '/' + transcript_id
    polling_response = requests.get(polling_endpoint, headers = headers)        # polling if the job is done
    return polling_response.json() 

def get_transcription_result_url(audio_url):                                    # checking the status regularly
    transcript_id = transcribe(audio_url)
    while True:
        data = poll(transcript_id)
        if data['status'] == 'completed':
            return data, None
        elif data['status'] == 'error':
            return data, data['error']
        print("Waiting for 30 secs...")
        time.sleep(30)

# save the transcribed data
def save_transcript(audio_url, filename):
    data, error = get_transcription_result_url(audio_url)
    if data:
        n = filename.index(".")
        file = filename[:n]
        outputtxt = file+".txt"
        with open(outputtxt, "w") as f:
            f.write(data['text'])
        print("Audio transcripted! Saved in the directory")
    else:
        print("Error!", error)




