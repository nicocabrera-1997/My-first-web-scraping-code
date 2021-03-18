import requests
import lxml.html as html
import os
import datetime

HOME_URL = 'https://www.cetrogar.com.ar/tecnologia/informatica/notebooks.html'

XPATH_LINK_TO_ARTICLE =  '//strong[@class="product name product-item-name"]/a[@class="product-item-link"]/@href'
XPATH_TITLE = '//div[@class="product-info-main"]/div[@class="page-title-wrapper product"]/h1[@class="page-title"]/span[@class="base"]/text()'
XPATH_DESCRIPTION = '//div[@class="toggle-container toggleValue attr-description active"]/div/div/div/p/text()'
XPATH_PRICE = '//span[@class="special-price"]//span[@class="price-wrapper "]/span[@class="price"]/text()'


def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notebooks = response.content.decode('utf-8')
            parsed  = html.fromstring(notebooks)

            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"', '')
                price = parsed.xpath(XPATH_PRICE)[0]
                descriptions = parsed.xpath(XPATH_DESCRIPTION)
            except IndexError:
                return

            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(f'Title: {title}')
                f.write('\n\n')
                f.write(f'Price: {price}')
                f.write('\n\n')
                for d in descriptions:
                    f.write(d)
                    f.write('\n')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notice = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            # print(links_to_notice)

            today = datetime.date.today().strftime('%Y-%m-%d') #guardamos la fecha
            if not os.path.isdir(today):
                os.mkdir(today)

            for link in links_to_notice:
                parse_notice(link, today)

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()


if __name__ == '__main__':
    run()
