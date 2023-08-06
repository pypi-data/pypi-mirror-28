import requests
from bs4 import BeautifulSoup

def get_genotype(stock_number):
    result = None
    urlpre = 'http://flybase.org/reports/FBst'
    url = urlpre + '{:07d}'.format(stock_number)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    ### finding genotype
    key = soup.find_all('div', class_='col-sm-3 col-sm-height field_label')
    value = soup.find_all('div', class_=['col-sm-9 col-sm-height', 'col-sm-3 col-sm-height'])
    for i, t in enumerate(key):
        if 'Stock List Description' in t.text:
            result = str(value[i].text)
    if result is None:
        print('Warning: stock number {} not found.'.format(stock_number))
    return result
