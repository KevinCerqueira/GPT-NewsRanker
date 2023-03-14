# Calendário interativo do semestre da UEFS (Calints)
A ideia do projeto é acessar a página que contem os links para baixar/visualizar os calendários dos semestres da UEFS (calendários esses em PDF), extrair o link de download/visualização e o nome de cada link, baixar os dois últimos semestre disponíveis (agora por exemplo os 2 últimos são o semestre de 2023.1 e 2023.2) processar e estruturar os dados, inserir no banco esses dados formatados e após isso criar uma API para disponibilizar via JSON esses dados, e criar um front-end para receber esses dados e montar um calendário bonito e interativo.

## LINKS
É somente 1 link, visto que a UEFS disponibiliza todos os calendários da história em uma unica página.
- [http://www.prograd.uefs.br/modules/conteudo/conteudo.php?conteudo=6](http://www.prograd.uefs.br/modules/conteudo/conteudo.php?conteudo=6)

## Esquema dos dados que serão extraídos
![esquema_dos_dados](https://github.com/KevinCerqueira/exa844-projeto-final/blob/main/banco_de_dados.png)

 - **calender**: tabela responsável por armazenar os dados dos dias e suas descrições
	 - id: ID único da tabela
	 - year: ano do dia e mês em questão
	 - month: ID da tabela **month**, que referencia o mês em questão
	 - day: o dia
	 - description: descrição do que vai acontecer no dia
 - **month**: tabela responsável por armazenar o nome do mês e o seu número respectivo
	 - id: ID único da tabela e número do mês
	 - month: nome do mês

## Parte dos dados extraídos do crawler
- Dados cru (RAW): ![exemplo_dados](https://github.com/KevinCerqueira/exa844-projeto-final/blob/main/exemplo_dados_extraidos.png)
- Dados processados e formatados em JSON:
``
{ "janeiro": { "01": "Feriado - Ano Novo", "02-31": "Férias docentes", "17-23": "Homologação das etapas da Matrícula Web (D.A.A. e Sistema Acadêmico)", "26/01-01/02": "Matrícula Web 2023.1" }, "fevereiro": { "01-06": "Preenchimento do Plano de Ensino das disciplinas no Portal Sagres", "01-12/02": "Preenchimento do PIT", "02-03": "Confirmação de matrícula (Sistema Acadêmico)", "02-08": "Planejamento Pedagógico" } }
``