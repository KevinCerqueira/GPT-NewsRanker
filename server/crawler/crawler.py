from bs4 import BeautifulSoup
import requests
import datetime
import pymysql
from gpt import Gpt
import core
import pymysql
from datetime import datetime
import time
from dotenv import load_dotenv
import os

class Crawler:
    def __init__(self) -> None:
        load_dotenv()
        self.chat = Gpt()
        self.conn, self.db = self.connect_database()
        self.main()
        
    def connect_database(self):
        try:
            config = {
                'user': os.getenv('DB_USERNAME'),
                'password': os.getenv('DB_PASSWORD'),
                'host': os.getenv('DB_HOST'),
                'database': os.getenv('DB_DATABASE'),
                'client_flag': pymysql.constants.CLIENT.PROTOCOL_41
            }
            conn = pymysql.connect(**config)
            return (conn, conn.cursor())
        except Exception as e:
            core.log_error(__class__.__name__ , str(e))
    
    def request_data(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
        
    def scraping_acordacidade(self, page = 1):
        url = 'https://www.acordacidade.com.br/noticias/page/' + str(page)
        core.log_debug('scraping_acordacidade', f'Requisitando site {url}')
        
        soup = self.request_data(url)
        news_all = soup.find_all("a", ({'class': 'noticia-3 card-archive'}))
        
        for news in news_all:
            # print(news_all)
            img = news.find('img')
            if(img is not None):
                img = img.get_attribute_list('src')[0]
            content = news.find('div', {'class': 'conteudo'})            
            date_raw = content.find('p', {'class': 'data-single'}).text
            date, hour = date_raw.split('às')
            
            data = {
                'external_id': news.attrs['id'],
                'title': news.attrs['title'],
                'category': content.find('h3', {'class': 'categoria'}).text,
                'date': str(datetime.strptime(date.strip() + hour.replace('h', ':') + ':00', '%d/%m/%Y %H:%M:%S')),
                'description': content.find('p', {'class': 'sub-text resumo-18'}).text,
                'link': news.attrs['href'],
                'image': img or "",
                'created_at': str(datetime.now())
            }
            
            try:
                result = bool(self.db.execute("SELECT 1 FROM news_ranker WHERE external_id = %s", (data['external_id'])))
                if(result):
                    continue
            except Exception as e:
                core.log_error("scraping_acordacidade [db.execute]" , str(e))
                continue

            
            time.sleep(3)
            response = self.chat.chat(os.getenv('TEXT_CHAT_DEFAULT') + "TITULO:" + data['title'] + " RESUMO:" + data['description'])
            if(os.getenv('TEXT_FINDER') not in response):
                time.sleep(3)
                response = self.chat.chat(os.getenv('TEXT_CHAT_DEFAULT') + data['title'] + os.getenv('TEXT_REINFORCEMENT'))
            
            if(os.getenv('TEXT_FINDER') not in response):
                core.log_error('scraping_acordacidade', f'Não foi possível ranquear a noticia {data["link"]}. Resposta do chatGPT: {response[:round(len(response)/4)]}...')
                continue
            
            core.log_debug('scraping_acordacidade', f'Resposta do chatGPT a noticia {data["link"]}: {response}')
            
            score = response[response.find(os.getenv('TEXT_FINDER'))+11:response.find(os.getenv('TEXT_FINDER'))+12]
            
            if(not score.isdigit()):
                time.sleep(3)
                response = self.chat.chat(os.getenv('TEXT_CHAT_DEFAULT') + data['title'] + os.getenv('TEXT_REINFORCEMENT'))
                score = response[response.find(os.getenv('TEXT_FINDER'))+11:response.find(os.getenv('TEXT_FINDER'))+12]
                if(not score.isdigit()):
                    core.log_error('scraping_acordacidade', f'Não foi possível ranquear a noticia {data["link"]}. Resposta do chatGPT: {response[:round(len(response)/4)]}...')
                    continue
            try:
                self.db.execute("""
                    INSERT INTO 
                        news_ranker (external_id, title, category, date, description, score, link, image, created_at) 
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);
                """, (data['external_id'], data['title'], data['category'], data['date'], data['description'], score, data['link'], data['image'], data['created_at']))
                self.conn.commit()
            except Exception as e:
                core.log_error("scraping_acordacidade [db.execute]" , str(e))
                exit()
                
    def main(self):
        for page in range(0,10):
            self.scraping_acordacidade(page)

if __name__ == "__main__":
    c = Crawler()
    exit()