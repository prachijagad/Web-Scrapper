from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import time

# Configuration
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (without GUI)
service = Service(r'Driver\chromedriver.exe')  # Replace with the path to your WebDriver

driver = webdriver.Chrome(service=service, options=chrome_options)

def fetch_static_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching static content from {url}: {e}")
        return None

def fetch_dynamic_content(url):
    try:
        driver.get(url)
        time.sleep(5)  # Wait for the page to fully load
        return driver.page_source
    except Exception as e:
        print(f"Error fetching dynamic content from {url}: {e}")
        return None

def parse_html(content):
    try:
        soup = BeautifulSoup(content, 'html.parser')
        return soup
    except Exception as e:
        print(f"Error parsing HTML content: {e}")
        return None

def scrape_content(soup):
    try:
        paragraphs = soup.find_all('header')
        for p in paragraphs:
            print(p.get_text())
    except Exception as e:
        print(f"Error scraping content: {e}")

def login(driver, login_url, username, password):
    try:
        driver.get(login_url)
        # Wait for the username field to be present and interactable
        WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.NAME, 'login'))
        ).send_keys(username)
        
        # Wait for the password field to be present and interactable
        WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.NAME, 'password'))
        ).send_keys(password)
        
        # Wait for the login button to be clickable and then click it
        WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.NAME, 'commit'))
        ).click()
        
        time.sleep(5)  # Wait for login to complete
    except Exception as e:
        print(f"Error logging in at {login_url}: {e}")

def crawl(urls, username=None, password=None, login_url=None, interval=10):
    visited_urls = set()
    for url in urls:
        if url not in visited_urls:
            print(f"Crawling: {url}")
            visited_urls.add(url)

            if username and password and login_url:
                try:
                    login(driver, login_url, username, password)
                except Exception as e:
                    print(f"Error during login: {e}")
                    continue

            try:
                if 'static' in url:
                    content = fetch_static_content(url)
                else:
                    content = fetch_dynamic_content(url)

                if content:
                    soup = parse_html(content)
                    if soup:
                        scrape_content(soup)
            except Exception as e:
                print(f"Error crawling {url}: {e}")

            time.sleep(interval)

if __name__ == "__main__":
    try:
        config = {
            "urls": [
                "https://github.com/settings/profile"  # Profile page URL after login
            ],
            "interval": 10,
            "username": "prachijagad",
            "password": "Theprachi308",
            "login_url": "https://github.com/login"
        }

        crawl(
            config['urls'],
            username=config.get('username'),
            password=config.get('password'),
            login_url=config.get('login_url'),
            interval=config['interval']
        )
    except Exception as e:
        print(f"An error occurred in the main block: {e}")
    finally:
        driver.quit()
