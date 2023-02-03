import scrapy
from datetime import datetime
from megafilmes.items import MegafilmesItem
import re

class megaSpider(scrapy.Spider):
    pesquisa = ""
    nomeArq = ""
    name = 'mega'

    # start_urls = [
    #https://megafilmesonline.org/assistir/filmes-de-todos/1
    # ]

    def start_requests(self):
        urls = [
            'https://megafilmesonline.org/assistir/filmes/lancamento/1'
        ]
        entrada = input('Digite o nome do ator:')
        if entrada is not None:
            self.pesquisa = entrada
        now = datetime.now()
        self.nomeArq = self.pesquisa + ' ' + str(now.day) + '-' + str(now.month) + '-' + str(now.year) + ' ' + str(
            now.hour) + ' ' + str(now.minute)
        print(self.nomeArq)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # direciona para pagina do Filme
        for href in response.css('div.generalMoviesList a::attr(href)'):
           # print("---- LINK Filme -----")
            #print(href.get())
            yield response.follow(href, self.parse_midia)
        #next page
        for href in response.xpath("//div[@class='paginationSystem']/a[@class='item click next']/@href"):# o for é por causa do retorne do response.
            #print("----Proxima Página-----")
            #print(href.get())
            yield response.follow(href, self.parse)

    def parse_midia(self, response):
        nomeFile = self.nomeArq
        print("---------------------PARSE MIDIA - -----------------------------")
        print(str(response.xpath("//div[@class='moviePresent']/h2/text()").get()).replace("\n",""))

        #Verificar se Contem o filtro de busca!
        if not (self.pesquisa.upper() in str(response.xpath("//span[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'elenco') and @class='prod']/b/text()").get()).upper()):
            return

        # Capturando a imagem - pega tudo após url:
        img_url = re.search(r"url\((.*)\)",
                            str(response.xpath("//style[contains(text(), 'background-image')]/text()").get())).group(1)

        #Criação do Item PipeLine
        midia = MegafilmesItem({
            'titulo': str(response.xpath("//div[@class='moviePresent']/h2/text()").get()).replace("\n",""),
            'ano': str(response.xpath("//div[@class='year']/b/text()").get()),
            'elenco': str(response.xpath("//span[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'elenco') and @class='prod']/b/text()").get()),
            'duracao': re.search(r"Duração:\s*(.*)", str(response.xpath("//span[@class='runtime']/text()").get()), re.IGNORECASE).group(1),
            'tipo': "Filme",
            'image_urls': [img_url],
            'link': response.url,
            "nomeArquivo":  nomeFile
        })

        with open(nomeFile + '.txt', 'a') as arq:
            arq.write(str(midia).replace("{", "").replace("}", ""))
            arq.write('\n|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\n')

        # vai para o pipeline ser tratado (automatico)
        yield midia