import requests
from bs4 import BeautifulSoup
import pandas as pd

# Read input from Excel sheet
input_file = 'Ebaycom-Input.xlsx'
df = pd.read_excel(input_file)
print (df.head())
# Function to scrape eBay
def scrape_ebay(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    items = []
    for item in soup.select('.s-item'):
        title = item.select_one('.s-item__title')
        price = item.select_one('.s-item__price')
        if title and price:
            items.append({
                'title': title.get_text(),
                'price': price.get_text()
            })
    return items

# Iterate over each search query in the Excel sheet
results = []
for index, row in df.iterrows():
    search_query = row['URL']
    items = scrape_ebay(search_query)
    print(f"Scraped {index} items from {search_query}")
    for item in items:
        results.append({
            'Keyword': row['Keyword'],
            'Product': item['title'],
            'Price': item['price'],
            'URL': search_query
        })

# Save results to a new Excel file
output_file = 'output.xlsx'
output_df = pd.DataFrame(results)
output_df.to_excel(output_file, index=False)

print(f"Scraping completed. Results saved to {output_file}")