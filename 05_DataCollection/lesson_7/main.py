#!python3
# -*- coding: utf-8 -*-



links = dom.xpath('//div[@data-qa-product]/a/@href')
pagination = dom.xpath('//div[@data-qa-pagination]//a/@href')
total_page = pagination[-2].split('=')[-1]

if pagination[-1] != pagination[-2]:
    pass

# Page
title = domp.xpath('//h1/text()')
price = domp.xpath('//meta[@itemprop="priceCurrency"]/../span/text()')
url = requests.url

# Props
props = domp.xpath('//div[@class="def-list__group"]')

def spec_transform(spec_list):
    specifications = {}
    for item in spec_list:
        item = item.xpath('.//text()')
        specifications[item[1].strip()] = item[3].strip()
    # del(item)
    print(specifications)



if __name__ == "__main__":
    pass
