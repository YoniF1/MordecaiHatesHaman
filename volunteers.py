import psycopg2
import config
from VolunteerManager import Manager

class MyVolunteer():
    def __init__(self,chat_id):
        self.chat_id = chat_id
        
    def run_query(self,query):
        Manager.run_query(query, False)

    def save(self):
        query = f"INSERT INTO our_volunteers(chat_id) VALUES('{self.chat_id}')"
        return self.run_query(query)

    def delete(self):
        query = f"DELETE FROM our_volunteers WHERE chat_id = '{self.chat_id}'"
        return self.run_query(query)

    def update(self, new_chat_id):
        query = f"UPDATE our_volunteers SET chat_id = '{new_chat_id}'WHERE chat_id = '{self.chat_id}' "
        return self.run_query(query)
    

