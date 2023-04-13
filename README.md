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
```json
{
   "SELECT * FROM news_ranker WHERE 1=1 ORDER BY score DESC":[
      {
         "id":34,
         "external_id":"post-280336",
         "title":"Vereadores fazem visita de surpresa a unidades municipais de saúde e constata denúncias",
         "category":"Feira de Santana",
         "date":"2023-04-13T01:45:00.000Z",
         "description":"A proposta partiu do vereador Luiz da Feira, membro da Comissão de Saúde da Casa, acatada pela presidente do Legislativo,...",
         "score":"8",
         "link":"https:\/\/www.acordacidade.com.br\/noticias\/dilton-e-feito\/vereadores-fazem-visita-de-surpresa-a-unidades-municipais-de-saude-e-constata-denuncias\/",
         "image":"https:\/\/imagens.acordacidade.com.br\/wp-content\/uploads\/2023\/04\/12224445\/visita-a-unidades-de-saude-327x204.jpg",
         "created_at":"2023-04-13T01:58:22.000Z",
         "updated_at":null,
         "deleted_at":null
      },
      {
         "id":58,
         "external_id":"post-280119",
         "title":"Formação de professores é entrave ao uso de tecnologia em sala de aula",
         "category":"Educação",
         "date":"2023-04-12T11:41:00.000Z",
         "description":"Estudo mostra ensino de ciência e tecnologia na educação básica brasileira.",
         "score":"8",
         "link":"https:\/\/www.acordacidade.com.br\/noticias\/educacao\/formacao-de-professores-e-entrave-ao-uso-de-tecnologia-em-sala-de-aula\/",
         "image":"https:\/\/imagens.acordacidade.com.br\/wp-content\/uploads\/2023\/04\/12083929\/home-office-notebook-computador-trabalhao-foto-marcelo-camargo-abr-09_07_2020_teletrabalho-4-327x204.jpg",
         "created_at":"2023-04-13T02:02:37.000Z",
         "updated_at":null,
         "deleted_at":null
      },
      {
         "id":43,
         "external_id":"post-280232",
         "title":"Secretaria de Meio Ambiente realiza fiscalização contra poluição visual",
         "category":"Feira de Santana",
         "date":"2023-04-12T19:31:00.000Z",
         "description":"Os principais alvos foram placas e cartazes instalados ilegalmente.",
         "score":"8",
         "link":"https:\/\/www.acordacidade.com.br\/noticias\/feira-de-santana\/secretaria-de-meio-ambiente-realiza-fiscalizacao-contra-poluicao-visual\/",
         "image":"https:\/\/imagens.acordacidade.com.br\/wp-content\/uploads\/2023\/04\/12162847\/SEMMAM-_-Poluicao-visual-327x204.jpeg",
         "created_at":"2023-04-13T02:01:31.000Z",
         "updated_at":null,
         "deleted_at":null
      },
      {
         "id":41,
         "external_id":"post-280216",
         "title":"Após cessão de uso do terreno do Centro de Convenções, Conder vai limpar e analisar estrutura do equipamento",
         "category":"Feira de Santana",
         "date":"2023-04-12T20:09:00.000Z",
         "description":"No espaço do Centro de Convenções existe um teatro, além de um pavilhão coberto, destinado a receber feiras e exposições....",
         "score":"8",
         "link":"https:\/\/www.acordacidade.com.br\/noticias\/feira-de-santana\/apos-cessao-de-uso-do-terreno-do-centro-de-convencoes-conder-vai-limpar-e-analisar-estrutura-do-equipamento\/",
         "image":"https:\/\/imagens.acordacidade.com.br\/wp-content\/uploads\/2022\/05\/26112049\/centro-de-convencoes-fotoe-ed-santos-acorda-cidade-2.jpg",
         "created_at":"2023-04-13T02:01:03.000Z",
         "updated_at":null,
         "deleted_at":null
      },
      {
         "id":61,
         "external_id":"post-280098",
         "title":"Sem cessão da área, vereador diz que Senar pode desistir de construir escola rural em Feira",
         "category":"Feira de Santana",
         "date":"2023-04-12T10:41:00.000Z",
         "description":"José Carneiro criticou a presidente da Câmara, Eremita Mota, por sugerir uma audiência pública para debater o assunto.",
         "score":"7",
         "link":"https:\/\/www.acordacidade.com.br\/noticias\/dilton-e-feito\/sem-cessao-da-area-vereador-diz-que-senar-pode-desistir-de-construir-escola-rural-em-feira\/",
         "image":"https:\/\/imagens.acordacidade.com.br\/wp-content\/uploads\/2023\/04\/12073921\/Vereador-Ze-Carneiro-Foto-Paulo-Jose-Acorda-Cidade-327x204.jpg",
         "created_at":"2023-04-13T02:02:52.000Z",
         "updated_at":null,
         "deleted_at":null
      }
   ]
}