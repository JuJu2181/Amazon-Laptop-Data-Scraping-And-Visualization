import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
import re
class AmazonProductSpider(scrapy.Spider):
    name = "amazon_product"
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

        title="nan"
        title=response.css("span.a-size-large.product-title-word-break::text").get()

        web_table = response.css('#productOverview_feature_div')
        for items in web_table:

            brand="nan"
            brand_row=items.css("tr.a-spacing-small.po-brand")            
            for value in brand_row:
                brand = value.css("span.po-break-word::text").get()
                    
            
            Screen_Size="nan"
            size_row = items.xpath("//tr[contains(@class, 'a-spacing-small po-display.size')]")
            for value in size_row:
                Screen_Size = value.xpath(".//span[contains(@class, 'a-size-base po-break-word')]/text()").get()

            Color="nan"
            color_row=items.css("tr.a-spacing-small.po-color")
            for value in color_row:
                Color = value.css("span.a-size-base.po-break-word::text").get()
                    
            series="nan"
            series_row=items.css("tr.a-spacing-small.po-model_name")
            for value in series_row:
                series = value.css("span.a-size-base.po-break-word::text").get()

            CPU_Model="nan"
            cpu_row = items.xpath("//tr[contains(@class, 'a-spacing-small po-cpu_model.family')]")
            for value in cpu_row:
                CPU_Model = value.xpath(".//span[contains(@class, 'a-size-base po-break-word')]/text()").get()

            Ram="nan"
            ram_row = items.xpath("//tr[contains(@class, 'a-spacing-small po-ram_memory.installed_size')]")
            for value in ram_row:
                Ram = value.xpath(".//span[contains(@class, 'a-size-base po-break-word')]/text()").get()

            Operating_System="nan"
            os_row=items.css("tr.a-spacing-small.po-operating_system")
            for value in os_row:
                Operating_System = value.css("span.a-size-base.po-break-word::text").get()

            Resolution="nan"
            res_row=items.css("tr.a-spacing-small.po-resolution")
            for value in res_row:
                Resolution =value.css("span.a-size-base.po-break-word::text").get()

            Battery="nan"
            bat_row = items.xpath("//tr[contains(@class, 'a-spacing-small po-battery.average_life')]")
            for value in bat_row:
                Battery = value.xpath(".//span[contains(@class, 'a-size-base po-break-word')]/text()").get()

            Weight="nan"
            wt_row=items.css("tr.a-spacing-small.po-item_weight")
            for value in wt_row:
                Weight = value.css("span.a-size-base.po-break-word::text").get()

            USB="nan"
            usb_row=items.css("tr.a-spacing-small.po-total_usb_ports")
            for value in usb_row:
                USB = value.css("span.a-size-base.po-break-word::text").get()

            Graphics="nan"
            graphics=items.css("tr.a-spacing-small.po-graphics_coprocessor")
            for value in graphics:
                Graphics = value.css("span.a-size-base.po-break-word::text").get()

            disk_size="nan"
            disksize = items.xpath("//tr[contains(@class, 'a-spacing-small po-hard_disk.size')]")
            for value in disksize:
                disk_size = value.xpath(".//span[contains(@class, 'a-size-base po-break-word')]/text()").get()

            card="nan"
            card_desc=items.css("tr.a-spacing-small.po-graphics_description")
            for value in card_desc:
                card = value.css("span.a-size-base.po-break-word::text").get()

            yield {
                "Title":title.strip(),
                "Brand": brand,
                "Screen_Size":Screen_Size,
                "CPU_Model":CPU_Model,
                "Ram":Ram,
                "Operating_System":Operating_System,
                "Rating":re.findall(r'(\d\.\d) out of 5',str(rating)),
                "Series":series,
                "Color":Color,
                "Resolution":Resolution,
                "Weight":Weight,
                "USB":USB,
                "Battery":Battery,
                "Graphics":Graphics,
                "Disk_size":disk_size,
                "Card_desc":card,
                "Price":price
            }