import os
import platform
from datetime import datetime
from datetime import date

# Arquivo para gravar o log nos arquivos

# Verificação se a plataforma é Linux ou outro
path_log = '/logs/log_'
if(platform.system() not in ['Linux', 'Darwin']):
	path_log = '\\logs\\log_'

# Grava mensagens no LOG do sistema (arquivo logs/log_ANO-MES-DIA.log)
def log(level, msg):
	with open(os.path.dirname(os.path.realpath(__file__)) + path_log + str(date.today()) + '.log', 'a', encoding='utf-8') as log_file:
		log_file.write("[{}] {}: {} \n".format(str(datetime.now()), level, msg))

def log_error(origin, msg):
	log('ERROR', origin + ": " + msg)

def log_info(origin, msg):
	log('INFO', origin + ": " + msg)

def log_debug(origin, msg):
	log('DEBUG', origin + ": " + msg)

def env(var):
	env = '\\.env'
	if(platform.system() in ['Linux', 'Darwin']):
		env = '/.env'
		
	with open(os.path.dirname(os.path.realpath(__file__)) + env, 'r', encoding='utf-8') as file_env:
		line = file_env.readline()
		while(line):
			content = line.split('=')
			if(content[0] == var):
				return content[1].replace('\n', '')
			line = file_env.readline()