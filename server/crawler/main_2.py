from bs4 import BeautifulSoup
import requests
import datetime
import urllib.request
from PyPDF2 import PdfReader
# from gpt import GPTClass
import json
class Crawler:
    def __init__(self) -> None:
        self.data = None
        self.year = datetime.datetime.now().year
        self.semesters = [f'{self.year}.1.pdf', f'{self.year}.2.pdf']
        # self.gpt = GPTClass()
        # self.request_data()
    
    def request_data(self) -> None:
        # url = 'https://drive.google.com/drive/folders/1QwnXl-Xq8EckfU3DwMARsgrcw1fQ0DTU'
        url = 'http://www.prograd.uefs.br/modules/conteudo/conteudo.php?conteudo=6'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup)
        # exit()
        self.process_data(soup=soup)

    def process_data(self, soup):
        h2_tag = soup.find_all('h2')
        a_tag = [h2.find('a') for h2 in h2_tag]
        first_semester = ''
        second_semester = ''
        for link in a_tag:
            if str(link).count(f'{self.year}.1') != 0:
                first_semester = link.get('href')
            elif str(link).count(f'{self.year}.2') != 0:
                second_semester = link.get('href')

            if(first_semester != '' and second_semester != ''):
                break
        
        urllib.request.urlretrieve(first_semester, self.semesters[0])
        urllib.request.urlretrieve(second_semester, self.semesters[1])
        self.read_pdf()

    def read_pdf(self):
        text_calender = ""
        months = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
        
        months_int = {1: "janeiro", 2: "fevereiro", 3: "março", 4: "abril", 5: "maio", 6: "junho", 7: "julho", 8: "agosto", 9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro"}
        
        calender = {"janeiro": [], "fevereiro": [], "março": [], "abril": [], "maio": [], "junho": [], "julho": [], "agosto": [], "setembro": [], "outubro": [], "novembro": [], "dezembro": []}
        for semester in self.semesters:
            with open(f'{semester}', 'rb') as pdf_file:
                
                pdf_reader = PdfReader(pdf_file)

                num_paginas = len(pdf_reader.pages)
                
                month = ''
                take_next_line = False
                start_day = ""
                start_month = ""
                current_month = ""
                for i in range(num_paginas):
                    page = pdf_reader.pages[i]
                    text = page.extract_text()
                    for line in text.split('\n'):
                        if '*' in line:
                            month = line[line.find('*'):line.find('\n')].replace(" ", "").replace('*', '').lower()
                            if(month in months):
                                current_month = month
                                continue
                        elif current_month != '':
                            if (line[1:3].isdigit()):
                                calender[current_month].append({'day': line[1:3], 'description': line[4:]})
                print(calender)       
    def contains_number(self, string):
        for char in string:
            if char.isdigit():
                return True
        return False          
    def get_data(self):
        return self.data
    

if __name__ == "__main__":
    cr = Crawler()
    cr.read_pdf()
    # print(cr.get_data())
    # print(type(cr.get_data()))