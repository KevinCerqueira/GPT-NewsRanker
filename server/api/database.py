import pymysql
import core
from datetime import datetime
from dotenv import load_dotenv
import os
class Database:
    def __init__(self) -> None:
        load_dotenv()

    def connect_database(self):
        try:
            config = {
                'user': os.getenv('DB_USERNAME'),
                'password': os.getenv('DB_PASSWORD'),
                'host': os.getenv('DB_HOST'),
                'database': os.getenv('DB_DATABASE'),
                'charset': 'utf8mb4'
            }
            conn = pymysql.connect(**config, cursorclass=pymysql.cursors.DictCursor)
            return (conn, conn.cursor())
        except Exception as e:
            core.log_error(__class__.__name__ , str(e))
    
    def get_news(self, args):
        query = "SELECT * FROM news_ranker WHERE 1=1"
        if 'description' in args:
            query += f" AND (description LIKE '%{args['description']}%' OR title LIKE '%{args['description']}%' OR category LIKE '%{args['description']}%')"
        if 'date_start' in args:
            query += f" AND date >= '{args['date_start']}'"
        if 'date_end' in args:
            query += f" AND date <= '{args['date_end']}'"
        if 'score'in args:
            query += f" AND score = '{args['score']}'"
            
        if 'order_score' in args:
            query += f" ORDER BY score {args['order_score']}"
        else:
            query += " ORDER BY score DESC"
        
        try:
            conn, db = self.connect_database()
            db.execute(query)
            data = []
            for row in db.fetchall():
                data.append({
                    'id': row['id'],
                    'title': row['title'],
                    'date': datetime.strftime(row['date'], '%Y-%m-%d %H:%M:%S'),
                    'description': row['description'],
                    'score': int(row['score']),
                    'newsUrl': row['link'],
                    'imageUrl': row['image']
                })
            return (True, data)
        except Exception as e:
            core.log_error('database.get_news', str(e) + ". query: " + query)
            return (False, str(e))
        
if __name__ == '__main__':
    c = Database()
    print(c.get_news({}))