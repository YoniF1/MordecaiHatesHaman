import config
import psycopg2
from googleapiclient.discovery import build

class Comments:
    def __init__(self):
        self.bad_words = set(['kike', 'shylock', 'coloniser', 'colonizer', 'from the river to the sea', 'zionazi', 'hitler', 'holocaust', 'rothschild', 'lehi', 'ethnic cleansing'])
        self.video_id = 'lJYn09tuPw4'

    def persist_to_database(self, comment, author_name, comment_id):
        query = f"""INSERT INTO comments(text, author, comment_id)
                VALUES ('{comment}', '{author_name}', '{comment_id}')"""
        
        self.run_query(query)

    def video_comments(self):
        youtube = build('youtube', 'v3', developerKey=config.DEVELOPERKEY)
        video_response = youtube.commentThreads().list(
            part='snippet,replies',
            videoId=self.video_id,
        ).execute()

        while video_response:
            for item in video_response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comment_id = item['snippet']['topLevelComment']['id']
                author_name = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
                replycount = item['snippet']['totalReplyCount']

                if any(word in comment for word in self.bad_words):
                    self.persist_to_database(comment, author_name, comment_id)
        
            if replycount > 0 and 'replies' in item:
                    replies = item['replies']['comments']
                    for reply in replies:
                        reply_text = reply['snippet']['textDisplay']
                        reply_author_name = reply['snippet']['authorDisplayName']
                        reply_id = reply['id']
                        if any(word in reply_text for word in self.bad_words):
                            self.persist_to_database(reply_text, reply_author_name, reply_id)

            if 'nextPageToken' in video_response:
                video_response = youtube.commentThreads().list(
                    part='snippet,replies',
                    videoId=self.video_id,
                    pageToken=video_response['nextPageToken']
                ).execute()
            else:
                break

    def run_query(self, query):
        conn = psycopg2.connect(host=config.HOSTNAME, user=config.USERNAME, dbname=config.DATABASE)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        conn.close()
        cursor.close
          

comments = Comments()
comments.video_comments()
