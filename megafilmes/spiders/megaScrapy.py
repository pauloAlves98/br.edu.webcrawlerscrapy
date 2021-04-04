import scrapy
from datetime import datetime
from megafilmes.items import MegafilmesItem


class megaSpider(scrapy.Spider):
    pesquisa = ""
    nomeArq = ""
    name = 'mega'

    # start_urls = [
    #     'https://megafilmes.org/page/1/?s'
    # ]

    def start_requests(self):
        urls = [
            'https://megafilmes.org/page/1/?s'
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

        # direciona para pagina do filme ou serie
        for href in response.css('div.item  h2.titulo a::attr(href)'):
            print("-------- Serie ou Filme ------")
            print(href.get())
            yield response.follow(href, self.parse_midia)
         #next page
        for href in response.xpath("//div[@class='pagination-wrap']/a[@class='next page-numbers']/@href"):# o for é por causa do retorne do response.
            #print("----Proxima Pagina-----")
            print(href.get())
            yield response.follow(href, self.parse)

    def parse_midia(self, response):
        nomeFile = self.nomeArq
        print("--------------------------------------------------")
        tipo = "Serie";
        if response.xpath("//div[@class='temporadas']").get() is None:
            tipo = "Filme"
        info = response.xpath("//div[@class='informacoes clearfix']/ul/li/b/text()").getall()
        iel = 3
        idur = 4
        print(info[2])
        if len(info) <= 0:
            return;

        if len(info) < 7:  # eh pq nao tem diretor
            if self.pesquisa.upper() in str(info[2]).upper():
                iel = 2
                idur = 3
            else:
                return
        elif self.pesquisa.upper() not in str(info[3]).upper():
            return
        img_url = response.css('div.capa  img::attr(src)').get()

        midia = MegafilmesItem({
            'titulo': (info[0]),
            'ano': str(info[1]),
            'elenco': info[iel],
            'duracao': info[idur],
            'tipo': tipo,
            #'image_urls': img_url,
            'link': response.url,
            "nomeArquivo":  nomeFile
            # 'nomeFile':nomeFile
        })

        with open(nomeFile + '.txt', 'a') as arq:
            # arq.write('Titulo:'+ (info[0])+'\n' +
            #             'Ano:'+str(info[1])+'\n' +
            #             'Elenco:' + info[iel]+'\n' +
            #             'Duracao:' + info[idur]+'\n' +
            #             'Tipo:' + tipo +'\n' +
            #             'img_url:' +  img_url  + '\n' +
            #             'Link:' +response.url+'\n')
            arq.write(str(midia).replace("{", "").replace("}", ""))
            arq.write('\n|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\n')

        yield MegafilmesItem({#vai para o pipeline ser tratado (automatico)
            'titulo': (info[0]),
            'ano': str(info[1]),
            'elenco': info[iel],
            'duracao': info[idur],
            'tipo': tipo,
            'image_urls': [img_url],
            'link': response.url,
            "nomeArquivo": nomeFile


            # 'nomeFile':nomeFile
        })
        # yield {
        #     'Titulo': info[0],
        #     'Ano':info[1],
        #     'Elenco': info[2],
        #     'Duracao': info[4],
        #     'Tipo': tipo,
        # }
