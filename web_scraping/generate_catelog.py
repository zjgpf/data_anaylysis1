import os
import pandas as pd
import bs4
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import re
from tqdm import tqdm
import pdb
import pickle

url_prefix = 'http://vip.stock.finance.sina.com.cn'
url_pattern = r'href=".+target='
title_pattern = r'_blank">.+</a>'
year_pattern = r'20[01][0-9]'

with open('code_set.pickle','rb') as f:
    codes = pickle.load(f)

def report_catelog(codes):
    reports = {
        'id':[],
        'code':[],
        'title':[],
        'url':[]       
    }
    for code in tqdm(codes):
        try:
            company_url = f'http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_Bulletin/stockid/{code}/page_type/ndbg.phtml'
            print(f'Processing {company_url}...')

            page_client = urlopen(company_url)
            page = page_client.read().decode('gbk')
            page_client.close()

            page_soup = soup(page, "html.parser")
            content = page_soup.find('div',{'class':'datelist'})

            all_url_title = content.findAll('a')


            current_id_set = set()
            for v in all_url_title:
                url = url_prefix + re.findall(url_pattern,str(v))[0][6:-9]
                url = url.replace('amp;','')          

                title = re.findall(title_pattern,str(v))[0][8:-4]
                year = re.findall(year_pattern, title)
                if not year: continue
                year = year[0]
                report_id = code+'_'+year
                if report_id in current_id_set: continue
                current_id_set.add(report_id)
                print(report_id)

                reports['code']+=[code]
                reports['title']+=[title]
                reports['id']+=[report_id]
                reports['url']+=[url]
        except Exception as e:
            print(e)
            continue
    return reports
        
catelog = report_catelog(codes)

df = pd.DataFrame(catelog)
df.to_csv('catelog.csv')
