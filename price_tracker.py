import requests
from bs4 import BeautifulSoup
import unicodedata

from send_email import send_email


HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})


def get_product_info(url):
    page = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(page.content, features="lxml")

    try:
        title = soup.find(id='productTitle').get_text().strip()
        price_str = soup.find(id='priceblock_ourprice').get_text()
    except:
        return None, None, None
    
    try:
        # #soup.select('#availability .a-color-price')[0].get_text().strip()
        soup.select('#availability .a-color-success')[0].get_text().strip()
        available = True
    except:
        available = False

    try:
        price = unicodedata.normalize("NFKD", price_str)
        price = price.replace(',', '.').replace('$', '')
        price = float(price)
    except:
        return None, None, None
    
    return title, price, available

if __name__ == '__main__':
    url = "https://www.amazon.com/Samsung-Factory-Unlocked-Smartphone-Pro-Grade/dp/B08FYTSXGQ/ref=sr_1_1_sspa?dchild=1&keywords=samsung%2Bs20&qid=1602529762&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExOTdFSllWVkhNMFRFJmVuY3J5cHRlZElkPUEwNDAyODczMktKMDdSVkVHSlA2WCZlbmNyeXB0ZWRBZElkPUEwOTc5NTcxM1ZXRlJBU1k1U0ZUSyZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU="
    products = [(url, 700)]
    
    products_below_limit = []
    for product_url, limit in products:
        title, price, available = get_product_info(product_url)
        if title is not None and price < limit and available:
            products_below_limit.append((url, title, price))


    if products_below_limit:
        message = "Subject: Price below limit!\n\n"
        message += "Your tracked products are below the given limit!\n\n"
        
        for url, title, price in products_below_limit:
            message += f"{title}\n"
            message += f"Price: {price}\n"
            message += f"{url}\n\n"
        
        send_email(message)
