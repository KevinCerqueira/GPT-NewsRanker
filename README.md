# Ranqueador de noticias

A ideia do projeto é acessar uma página de notícias (acorda cidade), capturar as noticias (informações como: titulo, descricao, data, etc) entregar ao chat GPT para dar uma nota, levando em consideração os critérios: relevância, Credibilidade, Impacto, Contextualização, Diversidade, Originalidade, Apelo emocional. Assim o chat GPT pontua em cada critério desse, de 0 a 10, e após isso faz uma pontuação final também de 0 a 10. Com isso disponibilizo as informações (a noticia e o score dela) e o usuario pode fazer filtragens de acordo com seu interesse.

  

## LINKS

Link do acorda cidade, é iterável como mostro abaixo:

- [https://www.acordacidade.com.br/noticias/page/0/](https://www.acordacidade.com.br/noticias/page/0/)
- [https://www.acordacidade.com.br/noticias/page/1/](https://www.acordacidade.com.br/noticias/page/1/)
- [https://www.acordacidade.com.br/noticias/page/2/](https://www.acordacidade.com.br/noticias/page/2/)
- por aí em diante...

  

## Esquema dos dados que serão extraídos

![esquema_dos_dados](https://github.com/KevinCerqueira/exa844-projeto-final/blob/main/esquema_dos_dados.png)
![banco_de_dados](https://github.com/KevinCerqueira/exa844-projeto-final/blob/main/banco_de_dados.png)
  

- **news_ranker**: tabela responsável por armazenar os dados das notícias

- id: ID único da tabela

- external_id: ID que o site da pra notícia

- title: título da notícia

- category: categoria da notícia sendo o site

- date: data da notícia segundo o site

- description: descrição/resumo da notícia

- score: pontuação que o ChatGPT deu aquela notícia

- link: link da notícia

- image: link da imagem da notícia

- created_at, updated_at,  deleted_at: datas de controles para o sistema

  

## Dados de 5 notícias de 1 iteração feita pelo crawler
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