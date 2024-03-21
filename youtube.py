import config
from googleapiclient.discovery import build

bad_words = ['kike', 'shylock', 'coloniser', 'colonizer', 'from the river to the sea', 'zionazi', 'hitler', 'holocaust', 'rothschild', 'lehi', 'ethnic cleansing']
bad_words_set = set(bad_words)
def write_to_file(text, author_name, comment_id):
    with open('youtube_replies.txt', 'a') as f:
        f.write(f"{text} \n{author_name}\n{comment_id}\n")

def video_comments(video_id):
    youtube = build('youtube', 'v3', developerKey=config.DEVELOPERKEY)
    video_response = youtube.commentThreads().list(
        part='snippet,replies',
        videoId='lJYn09tuPw4',
    ).execute()

    bad_words_set = set(bad_words)

    while video_response:
        for item in video_response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comment_id = item['snippet']['topLevelComment']['id']
            author_name = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
            replycount = item['snippet']['totalReplyCount']

            if any(word in comment for word in bad_words_set):
                write_to_file(comment, author_name, comment_id)
    
        if replycount > 0 and 'replies' in item:
                replies = item['replies']['comments']
                for reply in replies:
                    reply_text = reply['snippet']['textDisplay']
                    reply_author_name = reply['snippet']['authorDisplayName']
                    reply_id = reply['id']
                    if any(word in reply_text for word in bad_words_set):
                        write_to_file(reply_text, reply_author_name, reply_id)

        if 'nextPageToken' in video_response:
            video_response = youtube.commentThreads().list(
                part='snippet,replies',
                videoId=video_id,
                pageToken=video_response['nextPageToken']
            ).execute()
        else:
            break

video_id = "lJYn09tuPw4"
video_comments(video_id)