# This is a test spider for 2nd trial
import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
import re
class AmazonProductSpider(scrapy.Spider):
    name = "test"
    page_no = 1
    base_url = 'https://www.amazon.com'
    brands = ['lenovo','hp','asus','samsung','dell','microsoft','msi','acer','apple','alienware','gigabyte','generic','panasonic','lg','excaliberpc']
   
    # brands = ['lenovo','hp','asus']
    
    def start_requests(self):
        urls = []
        for brand in self.brands:
            urls.append(f"{self.base_url}/s?k={brand}+Laptop")
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)
       
    def parse(self,response):
        page=response
        laptops = response.css('div.s-result-item.s-asin')
        print(f"Total {len(laptops)} laptops found in this page")

        for link in response.css('a.a-link-normal.s-no-outline'):
            href = link.css('::attr(href)').get()
            if not href:
                continue
            yield response.follow(href, self.parse_product)
        for link in response.css('a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal'):
            href = link.css('::attr(href)').get()
            if not href:
                continue
            yield response.follow(href, self.parse_product)     

        next_page = response.css('a.s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator').attrib['href']
        next_page = f"{self.base_url}/{next_page}"
        print(f"temp:{next_page}")
        if next_page is not None:
            yield response.follow(next_page,callback=self.parse)    



    def parse_product(self, response):
        page = response 
        laptops = response.css('div.s-result-item.s-asin')
        print(f"Total {len(laptops)} laptops found in this page")

        price="nan"
        Price_Data=response.css('#corePriceDisplay_desktop_feature_div')
        for data in Price_Data:
            price=data.css('span.a-offscreen::text').get()

        rating="nan"
        rate=response.css("#averageCustomerReviews")
        for data in rate:
            rating=data.css("span.a-icon-alt::text").get()

        reviews="nan"
        review=response.css("#acrCustomerReviewText")
        for data in review:
            reviews=data.css("span.a-size-base::text").get()

        title="nan"
        title=response.css("span.a-size-large.product-title-word-break::text").get()


        web_table1 = response.css('#productDetails_techSpec_section_1')
        for items in web_table1:

            Screen_Size="nan"
            Screen_Size=items.css("tr:nth-child(1)>td:nth-child(2)::text").get()            
             
            Ram="nan"
            Ram=items.css("tr:nth-child(5)>td:nth-child(2)::text").get()   
            Chipset="nan"
            Chipset=items.css('th:contains(" Chipset Brand ") + td::text').get()     
            wireless="nan"
            wireless=items.css('th:contains("Wireless Type") + td::text').get()      
             
        web_table2 = response.css('#productDetails_techSpec_section_2')
        for items in web_table2:

            brand="nan"
            brand = items.css('th:contains("Brand") + td::text').get()

                  
            Color="nan"
            Color=items.css('th:contains("Color") + td::text').get()            
              
       
            series="nan"
            series=items.css('th:contains("Series") + td::text').get()            
        
            
            
            Weight="nan"
            Weight=items.css('th:contains("Item Weight") + td::text').get() 
            
            processor="nan"
            processor=items.css('th:contains("Number of Processors") + td::text').get() 
            
            

            flash="nan"
            flash=items.css('th:contains("Flash Memory Size") + td::text').get() 

            Battery="nan"
            Battery=items.css('th:contains("Batteries") + td::text').get() 
            

            def pre(info):
                cleaned = re.sub(r'^\s*\u200e([a-zA-Z0-9\s]+)$', r'\1', str(info)).strip()
                cleaned= str((re.sub(r'[^a-zA-Z0-9\s]', "", str(info))))
                # cleaned=re.sub(r'[a-zA-Z0-9\s]', "",cleaned)
                print(cleaned.strip())
                return cleaned.strip()
            # â€Ž
                
        
            yield {
                "Title":title.strip(),
                "Brand": pre(brand),
                "Screen_Size": pre(Screen_Size),
                "Ram":pre(Ram),
                "Series":pre(series),
                "Rating":rating,
                "Series":pre(series),
                "Color":pre(Color),
                "Chipset":pre(Chipset),
                "Wireless":pre(wireless),
                "Weight":pre(Weight),
                "No_of_Processor":pre(processor),
                "Flash_Memory":pre(flash),
                "Battery":pre(Battery),
                # "Disk_size":disk_size.,
                "No_of_Reviews":reviews,
                "Price":price
            }
