import request
from main import write_json
import re
#https://api.coinmarketcap.com/v1/ticker/bitcoin/
def parc_text(text)
    pattern = r'/\w+''
    crypto = re.search(pattern,text).group()
    return crypto[1:]
    #print(crypto)

def get_price(crypto):
    url='https://api.coinmarketcap.com/v1/ticker/{}}/'.format(crypto)
    r = requests.get(url).json()
    price = r[-1]['price_usd']
    #write_json(r.json(),filename='price.json')
    return price
def main():
    #get_price
    #parc_text()
    #priny(get_price(parc_text('сколько стоит /bitcoin?')))
if __name__ == '__main__':
    main()
