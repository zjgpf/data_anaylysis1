import os
import pandas as pd
import bs4
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import re
from tqdm import tqdm
import pdb
import pickle

root_dir = r'./content'
if not os.path.exists(root_dir): os.makedirs(root_dir)

def download_content(df):
    for v in tqdm(df.iterrows()):
        try:
            url = v[1]['url']
            file = os.path.join(root_dir,v[1]['id']+'.txt')
            print(f"Processing downloading {url}...")

            page_client = urlopen(url)
            page = page_client.read().decode('gbk')
            page_client.close()

            report_soup = soup(page, "html.parser", )

            content = str(report_soup.find('pre'))

            with open(file,'w') as f:
                f.write(content)
        except Exception as e:
            print(e)
            continue
        
df = pd.read_csv('catelog.csv')
download_content(df)
