import psycopg2
import config

class Manager:

    @staticmethod
    def run_query(query):
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
            result = cursor.fetchall()
            return result

        except psycopg2.Error as e:
            print('Error connecting', e)

        finally:
            if connection:
                cursor.close()
                connection.close()

    @classmethod
    def get_by_id(cls,chat_id):
        query = f"SELECT * FROM our_volunteers WHERE chat_id = '{chat_id}'"
        return cls.run_query(query)
    
    @classmethod
    def all(cls):
        query = f"SELECT * FROM our_volunteers"
        print (cls.run_query(query))