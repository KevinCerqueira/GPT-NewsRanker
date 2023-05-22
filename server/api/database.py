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
        if 'description' in args and args['description'] not in ('', None):
            query += f" AND (description LIKE '%{args['description']}%' OR title LIKE '%{args['description']}%' OR category LIKE '%{args['description']}%')"
        if 'date_start' in args and args['date_start'] not in ('', None):
            query += f" AND date >= '{args['date_start'].replace('+', '')}'"
        if 'date_end' in args and args['date_end'] not in ('', None):
            query += f" AND date <= '{args['date_end'].replace('+', '')}'"
        if 'score'in args and args['score'] not in ('', None):
            query += f" AND score = '{args['score']}'"
            
        if 'order_score' in args:
            query += f" ORDER BY score {args['order_score']}"
        else:
            query += " ORDER BY score DESC"
        
        if 'limit' in args and (isinstance(args['limit'], str) or isinstance(args['limit'], int)) and int(args['limit']) > 0:
            query += f" LIMIT {args['limit']}"
        else:
            query += " LIMIT 25"
            
        if 'offset' in args and (isinstance(args['offset'], str) or isinstance(args['offset'], int)) and int(args['offset']) > 0:
            query += f" OFFSET {args['offset']}"
        else:
            query += " OFFSET 0"
        try:
            conn, db = self.connect_database()
            core.log_debug("query: ", query)
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