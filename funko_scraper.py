from bs4 import BeautifulSoup
import requests
import urlmarker
import re


def get_product_details(url):
    # url = 'https://t.co/BhcCPznIN3'
    # url = 'https://t.co/cPvuoahssD'
    response = requests.get(url)
    html_soup = BeautifulSoup(response.text, "html.parser")
    product_containers = html_soup.find_all("div", {"class": "product-block"})
    details = []
    for each_product in product_containers:
        d = {}
        img_link = re.findall(urlmarker.WEB_URL_REGEX, str(each_product.img))
        product_link = (
            "https://www.funko-shop.com"
            + each_product.find_all("a", href=True)[0]["href"]
        )
        product_title = each_product.img["alt"]
        product_price = ((each_product.find("span", {"class": "price"})).text).strip()
        # print (((product_containers[0].find('span', {'class': 'price'})).text).strip())
        d["title"] = product_title
        d["link"] = product_link
        d["price"] = product_price
        d["img"] = "".join(img_link)
        # print (d['img'])
        details.append(d)
    return details


# get_product_details('https://t.co/UnPrSxQon2')
