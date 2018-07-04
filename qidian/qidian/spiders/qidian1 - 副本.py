# -*- coding: utf-8 -*-
import scrapy

from qidian.items import QidianItem
import enum
class Qidian1Spider(scrapy.Spider):
    name = 'qidian1'
    allowed_domains = ['qidian.com']
    start_urls = ['https://book.qidian.com/info/1010734492#Catalog']
    #https://book.qidian.com/info/1004608738#Catalog
    #https://book.qidian.com/info/1010734492#Catalog
    def parse(self, response):
        #div[@class="volume"][1或者2或者3或者4]中的数值，这些数值自定义一个变量替代，目前一共是4个部分，随着后续章节的增加，会出现第五部分或者第六部分 依次累加
        ###div[@class="volume"]["num"] ，num是自定义的变量，你可以换成自己想要的abc或者bb等变量，把这些变量放进去，就能得到所有章节的title？？（不知道为什么）
        for aa in response.xpath(
                '//div[@class="volume-wrap"]/div[@class="volume"]["'
                '这里填啥都行，不填就报错，或者去掉class=volume后面的这个中括号就得不到a标签中的标题，我也不知道什么原因！！！"]'
                '/ul[@class="cf"]/li'):
            #print(aa.extract())
            title=aa.xpath("a/text()").extract()
            #print(title)
            link=aa.xpath("a/@href").extract() ###得到一个list集合
            #print(link)
            #item=QidianItem()
            #item['title']=title
            #item['link']=link


            for new_link in link:
                new_links="https:"+str(new_link)
                #print(new_links)
                # yield scrapy.request(new_link,callback=self.parse_content)
                yield scrapy.Request(new_links, callback=self.parse_content)


    def parse_content(self,response):
        title_sum=[]
        for bb in response.xpath('//div[@class="main-text-wrap"]'):
            title=bb.xpath('//div[@class="text-head"]/h3[@class="j_chapterName"]/text()').extract()
            content = bb.xpath('//div[@class="read-content j_readContent"]/p/text()').extract()
            #print(title)
            ###切分list，得到空格的位置
            kong_list=list(''.join(title))
            #print(type(kong_list))
            a=' '
            if a in kong_list:  ###如果空格在这个list里面，则..
                kong_ge=list(''.join(title)).index(' ')###得到空格的下标位置
                #print(kong_list[1:kong_ge-1]) ###得到第几章里面的几章
                kong_ge_str="".join(kong_list[1:kong_ge-1])###list转换为str
                #print(kong_ge_str)
                title_sum.append(kong_ge_str)

            # else:
            #     print(kong_list)
            #title_sum.append(title)
            #####################得到的title是乱序的，此步骤要解决乱序的问题，要按照正序排列，开始########
            #print(title,len(title))
            ###我们打算用冒泡排序来解决这个问题###
            #####################得到的title是乱序的，此步骤要解决乱序的问题，要按照正序排列，结束########


        item=QidianItem()
        item['title']=title_sum    ######sort(reverse = False)  ###reverse = False 升序（默认）。sorted(n,key=lambda x:CN[x])
            #item['content']=content
        yield item

        #response.xpath('//div[@class="volume-wrap"]/div[@class="volume"][2]/ul[@class="cf"]/li/a/text()').extract()
        ###h:\python-virtualenv\daydaycode\lib\site-packages\parsel\selector.py", line 228, in xpath
        #####selector.xpath('//a[href=$url]', url="http://www.example.com")
