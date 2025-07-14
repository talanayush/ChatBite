import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def scrape_bikanervala_zomato():
    url = "https://www.zomato.com/ncr/bikanervala-1-raj-nagar-extension-ghaziabad/order"

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    time.sleep(4)

    # Expand all "Read More" descriptions
    try:
        while True:
            buttons = driver.find_elements(
                By.XPATH,
                "//span[contains(translate(text(), 'READ MORE', 'read more'), 'read more')]"
            )
            if not buttons:
                break
            for btn in buttons:
                try:
                    driver.execute_script("arguments[0].click();", btn)
                except:
                    pass
            time.sleep(0.5)
    except:
        pass

    page_src = driver.page_source
    driver.quit()
    
    soup = BeautifulSoup(page_src, "lxml")

    # Basic shop info
    rest = soup.find("h1")
    rest_name = rest.get_text(strip=True) if rest else ""
    loc_div = soup.find("div", class_=re.compile("sc-clNaTc"))
    location = loc_div.get_text(strip=True) if loc_div else ""
    phone_a = soup.find("a", href=re.compile(r"tel:"))
    contact = phone_a.get_text(strip=True) if phone_a else ""

    # Menu scraping
    menu_data = []
    sections = soup.find_all("section", class_=re.compile("sc-bZVNgQ"))
    for sec in sections:
        cat = sec.find("h4")
        category = cat.get_text(strip=True) if cat else ""
        items = sec.find_all("div", class_=re.compile("sc-jhLVlY"))
        for it in items:
            veg = "Unknown"
            vdiv = it.find("div", class_=re.compile("sc-gcpVEs"))
            if vdiv and vdiv.has_attr("type"):
                tv = vdiv["type"].lower()
                if "veg" in tv:
                    veg = "Veg"
                elif "non-veg" in tv:
                    veg = "Non‑Veg"

            nm = it.find("h4", class_=re.compile("sc-cGCqpu"))
            name = nm.get_text(strip=True) if nm else ""

            pr = it.find("span", class_=re.compile("sc-17hyc2s-1"))
            price = pr.get_text(strip=True) if pr else ""

            desc = ""
            dtag = it.find("p", class_=re.compile("sc-gsxalj"))
            if dtag:
                for rm in dtag.find_all("span", string=re.compile("read more", re.I)):
                    rm.extract()
                desc = dtag.get_text(" ", strip=True)

            spice = "Spicy" if re.search(r"spicy|fiery|peri peri|chilli|hot", desc, re.I) else "Normal"

            if name:
                menu_data.append({
                    "category": category,
                    "name": name,
                    "price": price,
                    "description": desc,
                    "veg_nonveg": veg,
                    "spice_level": spice
                })

    # Output
    print("Restaurant:", rest_name)
    print("Location:", location)
    print("Contact:", contact)
    print("Sample items:", menu_data[:3])

    df = pd.DataFrame(menu_data)
    df.to_csv("bikanervala_raj_nagar_extension_menu.csv", index=False)
    print("Saved to bikanervala_raj_nagar_extension_menu.csv")

if __name__ == "__main__":
    scrape_bikanervala_zomato()
