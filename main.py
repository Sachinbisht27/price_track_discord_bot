import os
import yaml
import sqlite3
import requests
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
def load_config():
    with open("config.yaml", "r") as file:
        return yaml.safe_load(file)

# Database setup
def init_db():
    conn = sqlite3.connect("prices.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            price REAL,
            last_checked TEXT
        )
    """)
    conn.commit()
    conn.close()
    logging.info("Database initialized.")

# Function to scrape price using Selenium
def scrape_price(url):
    logging.info(f"Scraping price for {url}")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    sleep(3)  # Give time for the page to load
    
    try:
        price_whole = driver.find_element(By.CSS_SELECTOR, "span.a-price-whole").text.replace(",", "")
        price_fraction = driver.find_element(By.CSS_SELECTOR, "span.a-price-fraction").text
        price = float(price_whole + "." + price_fraction)
        logging.info(f"Found price {price} for {url}")
        return price
    except Exception as e:
        logging.warning(f"Price not found for {url}: {e}")
        return None
    finally:
        driver.quit()

# Check for price drop
def check_price_drop(url, price):
    conn = sqlite3.connect("prices.db")
    cursor = conn.cursor()
    cursor.execute("SELECT price FROM prices WHERE url = ? ORDER BY last_checked DESC LIMIT 1", (url,))
    last_price = cursor.fetchone()
    
    if last_price and price < last_price[0]:
        logging.info(f"Price drop detected for {url}: {last_price[0]} -> {price}")
        return True
    
    cursor.execute("INSERT INTO prices (url, price, last_checked) VALUES (?, ?, ?)", (url, price, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    logging.info(f"Recorded new price {price} for {url}")
    return False

# Send Discord notification
def send_discord_alert(url, price, webhook_url):
    data = {
        "content": f"Price drop detected!\nProduct: {url}\nNew Price: ${price}"
    }
    response = requests.post(webhook_url, json=data, timeout=5)
    if response.status_code == 204:
        logging.info(f"Notification sent for {url}")
    else:
        logging.error(f"Failed to send notification for {url}, status code: {response.status_code}")

# Main function
def main():
    config = load_config()
    init_db()
    
    for product in config["products"]:
        url = product["url"]
        webhook_url = config["discord_webhook"]
        price = scrape_price(url)
        
        if price and check_price_drop(url, price):
            send_discord_alert(url, price, webhook_url)
    
if __name__ == "__main__":
    main()
