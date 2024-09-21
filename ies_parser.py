from bs4 import BeautifulSoup
import json

def parse_product_data(file_path):
    # Load the provided HTML file
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Initialize an empty list to hold product data
    products = []

    # Find all tables (potentially product listings) and iterate through each one
    tables = soup.find_all('table', {'bgcolor': 'WhiteSmoke'})

    for table in tables:
        rows = table.find_all('tr')

        # Ensure valid rows exist
        for row in rows:
            columns = row.find_all('td')

            if len(columns) >= 3:
                try:
                    # Extract relevant product details
                    product_id = columns[0].a['href'].split('(')[1].strip(')')
                    product_name = columns[2].text.strip()
                    manufacturer = columns[1].text.strip()
                    stock_code = columns[0].text.strip()

                    # Handle price extraction and convert to float
                    price_text = columns[-1].b.text.strip(' €:').replace(',', '')
                    price_in_euros = float(price_text) if price_text else None

                    # Identify category from the previous anchor tag
                    category_tag = table.find_previous('a', {'name': True})
                    category_name = category_tag.text.strip() if category_tag else "Unknown"

                    # Create product dictionary
                    product = {
                        "Category": category_name,
                        "Id": product_id,
                        "Name": product_name,
                        "Manufacturer": manufacturer,
                        "StockCode": stock_code,
                        "Brand": manufacturer,
                        "Description": product_name,
                        "PriceInEuros": price_in_euros,
                        "Link": f"http://products.iescomputers.com/details.asp?Stk_ID={product_id}"
                    }

                    # Append the product to the list
                    products.append(product)
                except Exception as e:
                    print(f"Error processing row: {columns}, Error: {e}")

    return products

def save_to_json(products, output_path):
    # Save products to a JSON file
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(products, file, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    input_html_path = 'dataFile.htm'  # Replace with actual file path
    output_json_path = 'output.json'  # Replace with desired output path

    # Parse product data from HTML
    products = parse_product_data(input_html_path)

    # Save parsed data to JSON
    save_to_json(products, output_json_path)

    # Output result
    print(f"Extracted {len(products)} products.")
