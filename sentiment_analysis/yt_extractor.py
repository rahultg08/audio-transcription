import youtube_dl

ydl = youtube_dl.YoutubeDL()                                        # creating an object of youtube_dl


def get_videoinfo(url):
    with ydl:
        result = ydl.extract_info(url, download=False)               # extracting the url of hosted file to pass into transcribe endpoint
    if "entries" in result:                                          # checking if the url is of playlist
        return result['entries'][0]                                  # if playlist, return the first video
    return result                                                    # else return the video pertaining to that url 

def get_audiourl(video_info):
    # print(video_info['formats'])                                   # printing the formats key-value pair of the video info dictionary (URLs)
    for f in video_info['formats']:
        # print(f['ext'])                                            # printing the extentions
        if f['ext'] == "m4a":                                        # check and return only those having extension as 'm4a'
            return f['url']


if __name__ == "__main__":
    video_info = get_videoinfo("https://www.youtube.com/watch?v=Ht90J5MwpUg")
    audio_url = get_audiourl(video_info)
    print(audio_url)