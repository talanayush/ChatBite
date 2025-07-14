import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def scrape_burgerking_zomato():
    url = "https://www.zomato.com/ncr/burger-king-raj-nagar-ghaziabad/order"

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    time.sleep(4)

    try:
        while True:
            read_more_buttons = driver.find_elements(By.XPATH, "//span[contains(translate(text(), 'READ MORE', 'read more'), 'read more')]")
            if not read_more_buttons:
                break
            for btn in read_more_buttons:
                try:
                    driver.execute_script("arguments[0].click();", btn)
                except Exception:
                    pass
            time.sleep(0.5)
    except Exception:
        pass

    soup = BeautifulSoup(driver.page_source, "lxml")
    driver.quit()

    rest_name = soup.find("h1")
    rest_name = rest_name.get_text(strip=True) if rest_name else ""
    location = ""
    loc_tag = soup.find("div", class_=re.compile("sc-clNaTc"))
    if loc_tag:
        location = loc_tag.get_text(strip=True)
    contact = ""
    phone_tag = soup.find("a", href=re.compile(r"tel:"))
    if phone_tag:
        contact = phone_tag.get_text(strip=True)

    menu_data = []
    menu_sections = soup.find_all("section", class_=re.compile("sc-bZVNgQ"))
    for section in menu_sections:
        cat_tag = section.find("h4")
        category = cat_tag.get_text(strip=True) if cat_tag else ""
        item_blocks = section.find_all("div", class_=re.compile("sc-jhLVlY"))
        for item in item_blocks:
            veg_type = "Unknown"
            veg_div = item.find("div", class_=re.compile("sc-gcpVEs"))
            if veg_div and veg_div.has_attr("type"):
                if veg_div["type"] == "veg":
                    veg_type = "Veg"
                elif veg_div["type"] == "non-veg":
                    veg_type = "Non-Veg"

            name_tag = item.find("h4", class_=re.compile("sc-cGCqpu"))
            name = name_tag.get_text(strip=True) if name_tag else ""

            price_tag = item.find("span", class_=re.compile("sc-17hyc2s-1"))
            price = price_tag.get_text(strip=True) if price_tag else ""

            desc_tag = item.find("p", class_=re.compile("sc-gsxalj"))
            desc = ""
            if desc_tag:
                for rm in desc_tag.find_all("span", string=re.compile("read more", re.I)):
                    rm.extract()
                desc = desc_tag.get_text(" ", strip=True)

            spice_level = "Spicy" if re.search(r"spicy|fiery|peri peri|chilli|hot", desc, re.I) else "Normal"

            if name:
                menu_data.append({
                    "category": category,
                    "name": name,
                    "price": price,
                    "description": desc,
                    "veg_nonveg": veg_type,
                    "spice_level": spice_level
                })

    print("Restaurant:", rest_name)
    print("Location:", location)
    print("Contact:", contact)
    print("Sample menu items:", menu_data[:3])

    df = pd.DataFrame(menu_data)
    df.to_csv("burgerking_raj_nagar_menu.csv", index=False)
    print("Saved to burgerking_raj_nagar_menu.csv")

if __name__ == "__main__":
    scrape_burgerking_zomato()
