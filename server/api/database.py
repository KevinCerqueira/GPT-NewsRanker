import pymysql
import core
from datetime import datetime
class Database:
    def connect_database(self):
        try:
            config = {
                'user': core.env('DB_USERNAME'),
                'password': core.env('DB_PASSWORD'),
                'host': core.env('DB_HOST'),
                'database': core.env('DB_DATABASE'),
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
                    'link': row['link'],
                    'image': row['image']
                })
            return (True, data)
        except Exception as e:
            core.log_error('database.get_news', str(e) + ". query: " + query)
            return (False, str(e))
        
if __name__ == '__main__':
    c = Database()
    print(c.get_news({}))