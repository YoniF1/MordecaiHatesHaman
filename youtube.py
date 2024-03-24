import config
import psycopg2
from googleapiclient.discovery import build

class Comments:
    def __init__(self, video_id):
        self.bad_words = set(['kike', 'shylock', 'coloniser', 'colonizer', 'from the river to the sea', 'zionazi', 'hitler', 'holocaust', 'rothschild', 'ethnic cleansing', 'terrorists'])
        self.video_id = video_id

    def persist_to_database(self, comment, author_name, video_id, comment_id, potentially_antisemitic = False):
        query = f"""INSERT INTO comments(text, author, video_id, comment_id, potentially_antisemitic)
                VALUES ('{comment}', '{author_name}', '{video_id}', '{comment_id}', {potentially_antisemitic})"""
        
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
                    self.persist_to_database(comment, author_name, self.video_id, comment_id, True)
                else:
                    self.persist_to_database(comment, author_name, self.video_id, comment_id)
        
            if replycount > 0 and 'replies' in item:
                    replies = item['replies']['comments']
                    for reply in replies:
                        reply_text = reply['snippet']['textDisplay']
                        reply_author_name = reply['snippet']['authorDisplayName']
                        reply_id = reply['id']
                        if any(word in reply_text for word in self.bad_words):
                            self.persist_to_database(reply_text, reply_author_name, self.video_id, reply_id, True)
                        else:
                            self.persist_to_database(comment, author_name, self.video_id, comment_id)
                        
            if 'nextPageToken' in video_response:
                video_response = youtube.commentThreads().list(
                    part='snippet,replies',
                    videoId=self.video_id,
                    pageToken=video_response['nextPageToken']
                ).execute()
            else:
                break

    def find_bad_comments(self):
        query = "SELECT * FROM comments WHERE potentially_antisemitic = True"
       
        comments = self.run_query(query, fetch_results=True)
        return comments

    def run_query(self, query, fetch_results=False):
        conn = psycopg2.connect(host=config.HOSTNAME, user=config.USERNAME, dbname=config.DATABASE)
        cursor = conn.cursor()
        cursor.execute(query)
        if fetch_results:
            result = cursor.fetchall()
        else:
            result = None
        conn.commit()
        conn.close()
        cursor.close
        return result

    
comments = Comments('8klRQ-zCVm4')
comments.video_comments()
# comments.find_bad_comments()
