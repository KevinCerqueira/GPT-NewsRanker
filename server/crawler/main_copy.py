from bs4 import BeautifulSoup
import requests
import datetime
import urllib.request
from PyPDF2 import PdfReader
from gpt import GPTClass
import json
class Crawler:
    def __init__(self) -> None:
        self.data = None
        self.year = datetime.datetime.now().year
        self.semesters = [f'{self.year}.1.pdf', f'{self.year}.2.pdf']
        # self.gpt = GPTClass()
        self.request_data()
    
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
        final_text = ''
        for semester in self.semesters:
            with open(f'{semester}', 'rb') as pdf_file:
                
                pdf_reader = PdfReader(pdf_file)

                num_paginas = len(pdf_reader.pages)
                
                month = ''
                take_next_line = False
                start_day = ""
                start_month = ""
                for i in range(num_paginas):
                    page = pdf_reader.pages[i]
                    text = page.extract_text()
                    
                    for line in text.split('\n'):
                        try:
                            if(line[0] == ' '):
                                line = line[1:]
                            if(not line[0].isdigit()):
                                final_text += line
                            else:
                                final_text += '\n' + line
                        except:
                            pass                
        print(final_text)
        for semester in self.semesters:
            with open(f'{semester}', 'rb') as pdf_file:
                
                pdf_reader = PdfReader(pdf_file)

                num_paginas = len(pdf_reader.pages)
                
                month = ''
                take_next_line = False
                start_day = ""
                start_month = ""
                for i in range(num_paginas):
                    page = pdf_reader.pages[i]
                    text = page.extract_text()
                    # for line in text.split('\n'):
                    for line in final_text:
                        if(take_next_line):
                            if(line[2:3] == "/"):
                                # calender[months_int[int(start_month)]].append(["start_day"] = start_day + "/" + start_month
                                end_day = line[0:2]
                                end_month = line[3:5]
                                description = line[5:]
                                final = start_day + "/" + start_month + "-" + end_day + "/" + end_month
                                # calender[months_int[int(start_month)]].append({"day": final, "description": description})
                                calender[month].append({"day": final, "description": description})
                                # calender[months_int[int(start_month)]]["end_day"] = start_day + "/" + start_month
                                # calender[months_int[int(start_month)]]["description"] = description
                                print(json.dumps(calender))
                            take_next_line = False
                        if('*' in line):
                            month = line[line.find('*'):line.find('\n')].replace(" ", "").replace('*', '').lower()
                        elif(month in months):
                            if(self.contains_number(line)):
                                if(line[0] == ' '):
                                    line = line[1:]
                                if(line[:2].isdigit()):
                                    if(line[2:3] == "/"):
                                        start_day = line[0:2]
                                        start_month = line[3:5]
                                        # print(calender[months_int[int(start_month)]])
                                        if(line[5:] == " a "):
                                            take_next_line = True
                                        # print(line[len(line)-2:])
                                        # if(line[8:] == '\n'):
                                        #     print(True)
                    # text_calender += text
                        
        # calender_json = self.gpt.chat("o texto abaixo é um calendário, separe os meses, dias e acontecimentos de cada dia num json (me retorno somente o json): \n {}".format(text))
        # teste = self.gpt.chat("o texto abaixo é um calendário, separe os meses, dias e acontecimentos de cada dia num json: \n {}".format(text))
        # print(text_calender)
        # print(calender_json)
    def contains_number(self, string):
        for char in string:
            if char.isdigit():
                return True
        return False          
    def get_data(self):
        return self.data
    

if __name__ == "__main__":
    cr = Crawler()
    # print(cr.get_data())
    # print(type(cr.get_data()))