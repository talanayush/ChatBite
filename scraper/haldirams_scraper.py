import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def scrape_haldirams_zomato():
    url = "https://www.zomato.com/ncr/haldirams-raj-nagar-ghaziabad/order"

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

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    driver.get(url)
    time.sleep(4)

    # Click all "Read More" buttons to expand item descriptions
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
                except Exception:
                    pass
                time.sleep(0.5)
    except Exception:
        pass

    soup = BeautifulSoup(driver.page_source, "lxml")
    driver.quit()

    # Restaurant metadata
    rest_name = soup.find("h1").get_text(strip=True) if soup.find("h1") else ""
    loc_tag = soup.find("div", class_=re.compile("sc-clNaTc"))
    location = loc_tag.get_text(strip=True) if loc_tag else ""
    phone_tag = soup.find("a", href=re.compile(r"tel:"))
    contact = phone_tag.get_text(strip=True) if phone_tag else ""

    # Scrape menu sections & items
    menu = []
    sections = soup.find_all("section", class_=re.compile("sc-bZVNgQ"))
    for sec in sections:
        cat = sec.find("h4").get_text(strip=True) if sec.find("h4") else ""
        items = sec.find_all("div", class_=re.compile("sc-jhLVlY"))
        for it in items:
            veg_flag = "Unknown"
            veg_div = it.find("div", class_=re.compile("sc-gcpVEs"))
            if veg_div and veg_div.has_attr("type"):
                tv = veg_div["type"].lower()
                veg_flag = "Veg" if "veg" in tv else "Non‑Veg" if "non‑veg" in tv else "Unknown"

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
                menu.append({
                    "category": cat,
                    "name": name,
                    "price": price,
                    "description": desc,
                    "veg_nonveg": veg_flag,
                    "spice_level": spice
                })

    # Output
    print("Restaurant:", rest_name)
    print("Location:", location)
    print("Contact:", contact)
    print("Sample menu items:", menu[:3])

    df = pd.DataFrame(menu)
    df.to_csv("haldirams_raj_nagar_menu.csv", index=False)
    print("Saved to haldirams_raj_nagar_menu.csv")

if __name__ == "__main__":
    scrape_haldirams_zomato()
