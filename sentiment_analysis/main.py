import json
from yt_extractor import get_audiourl, get_videoinfo
from api_comm import save_transcript


def save_sentiments(url):
    video_info = get_videoinfo(url)
    audio_url = get_audiourl(video_info)
    title = video_info['title']
    title = title.strip().replace(" ", "_")
    title = title[:-1]
    title = "sentiment_analysis/data/" + title
    save_transcript(audio_url, title, sentiment_analysis=True)


if __name__ == "__main__":
    # save_sentiments("https://www.youtube.com/watch?v=Ht90J5MwpUg")                              # to analyse the sentiments of each sentence spoken in the video

    with open("sentiment_analysis/data/Apple_iPhone_14_revie_sentiment.json", "r") as f:                             # loading the json file
        data = json.load(f)

    # creating lists to store each type of sentences
    positives = []                              
    negatives = []
    neutrals = []
    for result in data:
        text = result['text']
        if result['sentiment'] == "POSITIVE":
            positives.append(text)
        elif result['sentiment'] == "NEGATIVE":
            negatives.append(text)
        else:
            neutrals.append(text)
    
    # calculating length of each of the lists
    no_pos = len(positives)
    no_neg = len(negatives)
    no_neu = len(neutrals)

    print("Number of positives: ", no_pos)
    print("Number of negatives: ", no_neg)
    print("Number of neutrals: ", no_neu)

    r = no_pos/(no_pos+no_neg)                                              # calculate the positivity ratio ignoring neutrals
    print(f"Positive ratio: {r:.3f}")
