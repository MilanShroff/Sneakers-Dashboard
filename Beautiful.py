from lxml import html
import requests
import time


def select_brand(title):
    known_brands = [
        "Nike", "Adidas", "Puma", "Reebok", "New Balance", "Converse",
        "Jordan", "Asics", "Under Armour", "Vans", "Fila", "Skechers",
        "Brooks", "Saucony", "Mizuno", "Hoka", "Salomon", "Li-Ning",
        "Balenciaga", "Gucci", "Louis Vuitton", "Prada", "Versace", 
        "Alexander McQueen", "Chanel", "Dior", "Tom Ford", "Bape",
        "Veja", "Golden Goose", "On Running", "Allbirds", "APL", "Karhu", 
        "Yeezy", "Off-White", "Fear of God", "Maison Margiela",
        "DC Shoes", "Globe", "Supra", "Etnies", "Osiris", "Emerica",
        "Merrell", "Columbia", "The North Face", "Keen", "Altra"
    ]
    
    for brand in known_brands:
        if brand.lower() in title.lower():
            return brand
    return "Unknown"


def Price_Clean(price):
    if "to" in price:
        price = price.replace("$", "").replace(",", "").strip()
        parts = price.split("to")
        low = float(parts[0].strip())
        high = float(parts[1].strip())
        return round((low + high) / 2, 2)
    else:
        price = price.replace("$", "").replace(",", "").strip()
        try:
            return float(price)
        except ValueError:
            return 0.0


def Cost(shipping):
    if not shipping:
        return 0.0
    if "Free" in shipping:
        return 0.0
    shipping = shipping.replace('$', '').replace(',', '').strip()
    try:
        return float(shipping)
    except ValueError:
        return 0.0


def Country(Shipping_Country_str):
    if Shipping_Country_str and "from" in Shipping_Country_str:
        return Shipping_Country_str.replace("from", " ").strip()
    return "Unknown"


def scrape_ebay_sneakers_page(url):
    response = requests.get(url)
    tree = html.fromstring(response.content)
    
    items = tree.xpath('//li[contains(@class, "s-item")]')
    sneakers = [] 

    for item in items:
        
        title_list = item.xpath('.//div[@class="s-item__title"]//span/text()')
        title = title_list[0].strip() if title_list else "N/A"

        
        brand = select_brand(title)

        price_list = item.xpath('.//span[@class="s-item__price"]/text()')
        price_str = price_list[0].strip() if price_list else "0.0"
        price = Price_Clean(price_str)

        location_list = item.xpath('.//span[contains(@class, "itemLocation") or contains(@class, "s-item__location")]/text()')
        location_ctr = location_list[0].strip() if location_list else "N/A"
        location = Country(location_ctr)

        shipping_cost_list = item.xpath('.//span[contains(@class, "s-item__shipping")]/text()')
        shipping_cost_str = shipping_cost_list[0].strip() if shipping_cost_list else "0.0"
        shipping_cost = Cost(shipping_cost_str)

        condition_list = item.xpath('.//span[contains(@class, "SECONDARY_INFO")]/text()')
        condition = condition_list[0].strip() if condition_list else "N/A"

        sneakers.append({
            'title': title,
            'price': price,
            'location': location,
            'shipping_cost': shipping_cost,
            'condition': condition,
            'brand': brand,
        })

    return sneakers


def scrape_all_pages(base_url):
    all_data = [] 
    for page in range(1, 30):
        print(f"Scraping page {page}...")
        page_url = f"{base_url}&_pgn={page}"
        page_data = scrape_ebay_sneakers_page(page_url)
        all_data.extend(page_data)  
        time.sleep(1) 

    return all_data


base_url = "https://www.ebay.com/sch/i.html?_nkw=sneakers&_sacat=0&_from=R40&_trksid=p4432023.m570.l1313"
sneakers = scrape_all_pages(base_url)

print(f"Total items scraped: {len(sneakers)}")

