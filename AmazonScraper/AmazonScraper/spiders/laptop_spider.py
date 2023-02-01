import scrapy 

class LaptopSpider(scrapy.Spider):
    name = "laptop"
    page_no = 1
    base_url = 'https://www.amazon.com'
    brands = ['lenovo','hp','asus','samsung','dell','microsoft','msi','acer','apple','alienware','gigabyte','generic','panasonic','lg','excaliberpc']
    def start_requests(self):
        urls = []
        # urls = [f"{self.base_url}/s?k=Laptop"]
        # while self.page_no <= 20:
        #     urls.append(f'{self.base_url}&page={self.page_no}')
        #     self.page_no += 1
        for brand in self.brands:
            urls.append(f"{self.base_url}/s?k={brand}+Laptop")
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)
    
    def parse(self,response):
        page = response 
        laptops = response.css('div.s-result-item.s-asin')
        print(f"Total {len(laptops)} laptops found in this page")
        for laptop in laptops:
            name= laptop.css('span.a-text-normal::text').get()
            price_dollar = laptop.css('span.a-offscreen::text').get().replace('$','') if laptop.css('span.a-offscreen::text').get() else 0
            ratings = laptop.css('span.a-icon-alt::text').get()
            ratings = ratings.split()[0] if ratings else 0
            reviews = laptop.css('span.a-size-base.s-underline-text::text').get() if laptop.css('span.a-size-base.s-underline-text::text').get() else 0
            yield{
                'name': name,
                'price_dollar': price_dollar,
                'ratings': ratings,
                'reviews': reviews
            }
        # self.page_no+=1 
        # next_page = f'{self.base_url}&page={self.page_no+1}'
        next_page = response.css('a.s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator').attrib['href']
        next_page = f"{self.base_url}/{next_page}"
        # print(f"temp:{next_page}")
        if next_page is not None:
            yield response.follow(next_page,callback=self.parse)