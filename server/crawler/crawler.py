from bs4 import BeautifulSoup
import requests
import datetime
import pymysql
import os
import platform
from gpt import Gpt
import core
import pymysql
from datetime import datetime

class Crawler:
    def __init__(self) -> None:
        self.main()
        
    def connect_database(self):
        try:
            config = {
                'user': core.env('DB_USERNAME'),
                'password': core.env('DB_PASSWORD'),
                'host': core.env('DB_HOST'),
                'database': core.env('DB_DATABASE'),
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
        conn, db = self.connect_database()
        
        for news in news_all:
            
            img = news.find('img')
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
                'image': img.get_attribute_list('src')[0],
                'created_at': str(datetime.now())
            }
            
            try:
                result = bool(db.execute("SELECT 1 FROM news_ranker WHERE external_id = %s", (data['external_id'])))
                if(result):
                    continue
            except Exception as e:
                core.log_error("scraping_acordacidade [db.execute]" , str(e))
                continue

            
            gpt = Gpt()
            response = gpt.chat(core.env('TEXT_CHAT_DEFAULT') + data['title'])
            if(core.env('TEXT_FINDER') not in response):
                response = gpt.chat(core.env('TEXT_CHAT_DEFAULT') + data['title'] + core.env('TEXT_REINFORCEMENT'))
            
            if(core.env('TEXT_FINDER') not in response):
                core.log_error('scraping_acordacidade', f'Não foi possível ranquear a noticia {data["link"]}. Resposta do chatGPT: {response[:round(len(response)/4)]}...')
                continue
            
            core.log_debug('scraping_acordacidade', f'Resposta do chatGPT a noticia {data["link"]}: {response}')
            
            score = response[response.find(core.env('TEXT_FINDER'))+11:response.find(core.env('TEXT_FINDER'))+12]
            
            if(not score.isdigit()):
                response = gpt.chat(core.env('TEXT_CHAT_DEFAULT') + data['title'] + core.env('TEXT_REINFORCEMENT'))
                score = response[response.find(core.env('TEXT_FINDER'))+11:response.find(core.env('TEXT_FINDER'))+12]
                if(not score.isdigit()):
                    core.log_error('scraping_acordacidade', f'Não foi possível ranquear a noticia {data["link"]}. Resposta do chatGPT: {response[:round(len(response)/4)]}...')
                    continue
            try:
                db.execute("""
                    INSERT INTO 
                        news_ranker (external_id, title, category, date, description, score, link, image, created_at) 
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);
                """, (data['external_id'], data['title'], data['category'], data['date'], data['description'], score, data['link'], data['image'], data['created_at']))
                conn.commit()
            except Exception as e:
                core.log_error("scraping_acordacidade [db.execute]" , str(e))
                exit()
                
    def main(self):
        for page in range(1,4):
            self.scraping_acordacidade(page)

if __name__ == "__main__":
    c = Crawler()
    exit()