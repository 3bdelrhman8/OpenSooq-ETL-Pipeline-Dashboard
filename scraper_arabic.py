import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import datetime
import time
import random
from sqlalchemy import create_engine

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "ar,en-US;q=0.9,en;q=0.8"
}

data = []
pages_to_scrape = 22

print(f"Starting extraction for {pages_to_scrape} pages...")

for page in range(1, pages_to_scrape + 1):
    print(f"Scraping page {page}...")
    url = f"https://eg.opensooq.com/ar/find?term=iphone&page={page}"
    
    try:
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        items = soup.find_all('div', class_='borderBottomDashed') 
        
        for item in items:
            title_element = item.find('h2', class_='font-15 bold trimTwoLines')
            price_element = item.find('div', class_='redColor bold font-18')
            
            if title_element and price_element:
                title = title_element.text.strip()
                price_text = price_element.text.strip()
                
                data.append({
                    'Product': title,
                    'Price_Raw': price_text,
                    'Date_Scraped': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                
    except Exception as e:
        
        print(f"Connection error on page {page}. Skipping to next page...")
        

    time.sleep(random.uniform(2, 5))

df = pd.DataFrame(data)

print("Transforming Arabic data...")
def clean_arabic_price(price_str):
    cleaned = re.sub(r'[^\d]', '', price_str)
    try:
        return float(cleaned)
    except ValueError:
        return None

if not df.empty:
    df['Price_Cleaned'] = df['Price_Raw'].apply(clean_arabic_price)
    df.dropna(subset=['Price_Cleaned'], inplace=True)
    
    print("Loading into MySQL Database...")
    engine = create_engine("mysql+pymysql://root:Ahmed258%23@localhost/arabic_market")
    
    df.to_sql("opensooq_iphones", con=engine, if_exists="replace", index=False)
    print(f"Success! Scraped and saved {len(df)} phones to MySQL (arabic_market)")
else:
    print("No data extracted. Please check your connection or HTML classes.")