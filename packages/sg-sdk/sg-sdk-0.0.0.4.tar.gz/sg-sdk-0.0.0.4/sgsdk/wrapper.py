import re
import json
import urllib
from bs4 import BeautifulSoup as bs
from aio import ApiWrapper

class Variant(object):
    def __init__(self, variant_data):
        self.size = variant_data['size']
        self.price = variant_data['price']
        self.in_stock = variant_data['in_stock']

class SearchProduct(object):
    def __init__(self, product_data):
        self.title = product_data['title']
        self.sku = product_data['sku']
        self.image = product_data['image']
        self.variants = [Variant(v) for v in product_data['variants']]

class Product(object):
    def __init__(self, product_data):
        self.pid = product_data['pid']
        self.title = product_data['title']
        self.sku = product_data['sku']
        self.status = product_data['status']
        self.size = product_data['size']
        self.warehouse = product_data['warehouse']
        self.condition = product_data['condition']
        self.in_stock_time = product_data['in_stock_time']
        self.price = product_data['price']
        self.return_amount = str(round((float(self.price.replace('$','')) * 0.8), 2))
        self.price_range = product_data['price_range']
        self.last_sale = product_data['last_sale']
        self.image = product_data['image']

class PayoutProduct(object):
    def __init__(self, product_data):
        self.pid = product_data['pid']
        self.title = product_data['title']
        self.sku = product_data['sku']
        self.status = product_data['status']
        self.size = product_data['size']
        self.intake_date = product_data['intake_date']
        self.sold_date = product_data['sold_date']
        self.sold_price = product_data['sold_price']
        self.return_amount = str(round((float(self.sold_price.replace('$','')) * 0.8), 2))
        self.image = product_data['image']

class StadiumGoods(ApiWrapper):
    BASE_URL = 'https://sellers.stadiumgoods.com'

    def __get_login_auth_token(self):
        endpoint = '/'
        response = self.get(endpoint)
        soup = bs(response.text, 'html.parser')
        auth_token = soup.find('input', {'name': 'authenticity_token'})['value']
        return auth_token

    def authenticate(self, username, password):
        endpoint = '/users/sign_in'
        payload = {
            'authenticity_token': self.__get_login_auth_token(),
            'commit': 'Login',
            'user[email]': username,
            'user[password]': password,
            'user[remember_me]': 1,
            'utf8': '✓'
        }
        response = self.post(endpoint, data=payload)
        success = 'Signed in successfully.' in response.text
        return success

    def get_pending_payout_items(self):
        endpoint = '/sellers/reports/pending_payout'
        response = self.get(endpoint)
        soup = bs(response.text, 'html.parser')
        product_rows = soup.find_all('tr')[1:]
        products = []
        for product_row in product_rows:
            image = product_row.find('img')['src']
            headers = [h.get_text() for h in product_row.find_all('h5')]
            sku_pattern = r'%7C(.*?)&'
            products.append(PayoutProduct({
                'pid': headers[1],
                'title': headers[0],
                'sku': urllib.parse.unquote(re.search(sku_pattern, image).group(1)),
                'status': headers[2],
                'size': headers[3],
                'intake_date': headers[4],
                'sold_date': headers[5],
                'sold_price': headers[6],
                'image': image
            }))
        return products

    def get_pending_payout(self):
        pending_payout_items = self.get_pending_payout_items()
        return str(round(sum(float(i.return_amount) for i in pending_payout_items), 2))

    def get_inventory(self):
        endpoint = '/sellers/price_updates/new?page_size=All'
        response = self.get(endpoint)
        soup = bs(response.text, 'html.parser')
        product_divs = soup.find_all('adjust-price-container')
        products = []
        for product_div in product_divs:
            try:
                product_data = json.loads(urllib.parse.unquote(product_div[':serial']))
            except:
                # SG sometimes defaults to legacy backend
                product_data = {
                    'id': product_div['data-id'],
                    'sku': product_div['data-sku'],
                    'size': product_div['data-size']
                }
            status_div = product_div.find('div', {'class': 'adjustPrice-status'})
            status_headers = status_div.find_all('h5')
            warehouse_pattern = r'At (.*?) warehouse'
            condition_div = product_div.find_all('div', {'class': 'col-sm-2'})[1]
            condition_headers = condition_div.find_all('h5')
            in_stock_time_pattern = r'In stock for(?: about)?(?= \d) (.*)'
            price_div = product_div.find('div', {'class': 'adjustPrice-text-price'})
            price_spans = price_div.find_all('span')
            price_range_pattern = r'Current price range: (.*)'
            last_sale_pattern = r'Last Sale:.*?(?=\d|not)(.*)(?<=\d)'
            products.append(Product({
                'pid': product_data['id'],
                'title': product_div.find('h4').get_text(),
                'sku': product_data['sku'],
                'status': status_headers[0].get_text(),
                'size': product_data['size'],
                'warehouse': re.search(warehouse_pattern, status_headers[1].get_text()).group(1),
                'condition': condition_headers[0].get_text(),
                'in_stock_time': re.search(in_stock_time_pattern, condition_headers[1].get_text()).group(1),
                'price': product_div.find('input', {'name': 'price'})['data-orig-price'],
                'price_range': re.search(price_range_pattern, price_spans[0].get_text()).group(1),
                'last_sale': re.search(last_sale_pattern, price_spans[1].get_text(), re.DOTALL).group(1),
                'image': product_div.find('img')['src']
            }))
        return products

    def get_under_review(self):
        inventory = self.get_inventory()
        return [i for i in inventory if i.status == 'Under Review']

    def get_product_by_sku(self, sku):
        endpoint = 'https://www.stadiumgoods.com/search/go'
        params = {
            'w': sku
        }
        response = self.get(endpoint, params=params)
        soup = bs(response.text, 'html.parser')
        variant_divs = soup.find_all('div', {'itemprop': 'offers'})
        variants = []
        for variant_div in variant_divs:
            variants.append({
                'size': variant_div.find('span', {'itemprop': 'name'}).get_text().split(' - ')[1],
                'price': variant_div.find('span', {'itemprop': 'price'}).get_text(),
                'in_stock': 'InStock' in variant_div.find('link', {'itemprop': 'availability'})['href']
            })
        product = SearchProduct({
            'title': soup.find('h1', {'class': 'product-name'}).get_text(),
            'sku': soup.find('meta', {'itemprop': 'sku'})['content'],
            'image': soup.find('img')['src'],
            'variants': variants
        })
        return product
        