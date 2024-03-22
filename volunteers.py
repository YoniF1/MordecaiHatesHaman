import psycopg2
import config

class MyVolonteer():
    def __init__(self,chat_id):
        self.chat_id = chat_id
        
    def run_query(self,query):
        try:
            connection = psycopg2.connect(
                host=config.HOSTNAME,
                user=config.USERNAME,
                password=config.PASSWORD,
                dbname=config.DATABASE,
                port=config.PORT
            )
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
        

        except psycopg2.Error as e:
            print('Error connecting', e)

        finally:
            if connection:
                cursor.close()
                connection.close()

    def save(self):
        query = f"INSERT INTO our_volunteers(chat_id) VALUES('{self.chat_id}')"
        return self.run_query(query)

    def delete(self):
        query = f"DELETE FROM our_volunteers WHERE chat_id = '{self.chat_id}'"
        return self.run_query(query)

    def update(self, new_chat_id):
        query = f"UPDATE our_volunteers SET chat_id = '{new_chat_id}'WHERE chat_id = '{self.chat_id}' "
        return self.run_query(query)
    

