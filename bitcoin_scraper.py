from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Selenium options
options = Options()
options.add_argument("--headless")  # Enable headless mode for GitHub Actions
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

# Rotate User-Agent to prevent detection
ua = UserAgent()
options.add_argument(f"user-agent={ua.random}")

# Set up ChromeDriver using webdriver_manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Define the target website (CoinMarketCap Bitcoin page)
URL = "https://coinmarketcap.com/currencies/bitcoin/"

def scrape_bitcoin_data():
    """Scrape Bitcoin details from CoinMarketCap."""
    driver.get(URL)
    time.sleep(10)  # Allow time for elements to load

    try:
        # Extract Bitcoin Price
        price = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//span[@data-test="text-cdp-price-display"]'))
        ).text

        # Extract Market Cap
        market_cap = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, "//dt[.//div[contains(text(),'Market cap')]]/following-sibling::dd//span")
            )
        ).text

        # Extract 24h Trading Volume
        volume_24h = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, "//dt[.//div[contains(text(),'Volume (24h')]]/following-sibling::dd//span")
            )
        ).text

        # Extract Circulating Supply
        circulating_supply = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, "//dt[.//div[contains(text(),'Circulating supply')]]/following-sibling::dd//span")
            )
        ).text

        # Extract 24h Price Change
        price_change_24h = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(@class, 'change-text')]") )
        ).text

        # Extract Community Sentiment
        bullish_sentiment_elems = driver.find_elements(By.XPATH,
                                                       "//span[contains(@class, 'sc-65e7f566-0 cOjBdO') and contains(@class, 'ratio')]")
        bearish_sentiment_elems = driver.find_elements(By.XPATH,
                                                       "//span[contains(@class, 'sc-65e7f566-0 iKkbth') and contains(@class, 'ratio')]")

        bullish = bullish_sentiment_elems[0].text if bullish_sentiment_elems else "N/A"
        bearish = bearish_sentiment_elems[0].text if bearish_sentiment_elems else "N/A"

        # Capture timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Store the data in a dictionary
        bitcoin_data = {
            "timestamp": timestamp,
            "price": price,
            "market_cap": market_cap,
            "volume_24h": volume_24h,
            "circulating_supply": circulating_supply,
            "price_change_24h": price_change_24h,
            "bullish_sentiment": bullish,
            "bearish_sentiment": bearish
        }

        return bitcoin_data

    except Exception as e:
        print("Error occurred:", e)
        return None

def save_to_csv(data):
    """Save scraped data to CSV."""
    file_name = "bitcoin_hourly_data.csv"
    try:
        df = pd.read_csv(file_name)
    except FileNotFoundError:
        df = pd.DataFrame(columns=[
            "timestamp", "price", "market_cap", "volume_24h",
            "circulating_supply", "price_change_24h", "bullish_sentiment", "bearish_sentiment"
        ])

    # Create a DataFrame for the new data row
    new_row = pd.DataFrame([data])

    # Concatenate the new row to the existing DataFrame
    df = pd.concat([df, new_row], ignore_index=True)

    # Save back to CSV
    df.to_csv(file_name, index=False)

if __name__ == "__main__":
    print("Scraping Bitcoin Data...")
    scraped_data = scrape_bitcoin_data()

    if scraped_data:
        save_to_csv(scraped_data)
        print("Data saved to bitcoin_hourly_data.csv")
    else:
        print("Failed to scrape data.")

    driver.quit()
