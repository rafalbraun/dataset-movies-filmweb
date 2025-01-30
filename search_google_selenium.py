from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver_path = "/usr/bin/chromedriver"

def google_search(search_query):
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
    # options.add_argument("--headless")
    # options.add_argument("--disable-gpu")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(driver_path, options=options)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
        """
    })

    try:
        driver.get("https://www.google.com")
        time.sleep(2)

        try:
            accept_button = driver.find_element(By.XPATH, "//button[contains(., 'Zaakceptuj wszystko') or contains(., 'Accept all')]")
            accept_button.click()
            print("Zaakceptowano cookies.")
        except Exception as e:
            print("Nie znaleziono przycisku cookies lub wystąpił błąd:", e)

        search_box = driver.find_element(By.NAME, "q")

        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)

        time.sleep(2)

        search_results_container = driver.find_element(By.ID, "rso")
        search_results = search_results_container.find_elements(By.TAG_NAME, "a")

        # for index, result in enumerate(search_results, start=1):
        #     print(f"{index}. {result.get_attribute('href')}")

        result_links = []
        for result in search_results:
            result_links.append(result.get_attribute('href'))
        return result_links

    except Exception as e:
        print(f"Nie udało się znaleźć elementu 'rso' lub zebrać linków. Błąd: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    search_query="Buntownicy, gwiazdy, rewelucjoniści! Ashe, McEnroe, Borg, King, Navratilova, Evert na zawsze odmienili oblicze tenisa. Stali się legendami tego sportu, ale walczyli także poza kortem. Odważnie przekraczali granice i mieli odwagę zmieniać świat. Twórcy programu przedstawiają złotą erę tenisa przez pryzmat turnieju w Wimbledonie."
    google_search(search_query)
