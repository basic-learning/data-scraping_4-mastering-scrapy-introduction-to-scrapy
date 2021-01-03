import scrapy


class RwidSpider(scrapy.Spider):
    name = 'rwid'
    allowed_domains = ['167.172.70.208']
    start_urls = ['http://167.172.70.208:9999/']

    def parse(self, response):
        data : {
            'username':'user',
            'password':'user12345'
        }
        return scrapy.FormRequest(
            url='http://167.172.70.208:9999/login',
            formdata=data,
            callback=self.after_login
        )
    def after_login(self, response):
        """
        1. Ambil semua data barang yang ada di halaman hasil -> akan menuju detail (parsing detail)
        2. Ambil semua link next -> akan kembali ke self.after_login
        """
        # Get detail products
        detail_products: List[Selector] = response.css('.card .card-title a')
        for detail in detail_products:
            href = detail.attrib.get('href')
            yield response.follow(href, callback=self.parse_detail)
        yield {'title':response.css('title::text').get()}
        paginations: List[Selector] = response.css('.pagination a.page-link')
        for pagination in paginations:
            href = pagination.attrib.get('href')
            yield response.follow(href, callback=self.after_login)
    def parse_detail(self,response):
        image = response.css('.card-img-top').attrib.get('src')
        title = response.css('.card-title::text').get()
        stock = response.css('.card-stock::text').get()
        description = response.css('.card-text::text').get()
        return {
            'image':image,
            'title':title,
            'stock':stock,
            'desc':description
        }