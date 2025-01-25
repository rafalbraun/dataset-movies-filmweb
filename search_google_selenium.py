from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Ścieżka do WebDriver (dostosuj do swojej lokalizacji)
driver_path = "/usr/bin/chromedriver"

def google_search(search_query):
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("--headless")  # Tryb bez okna
    # options.add_argument("--disable-gpu")  # Dla kompatybilności (Windows)
    # options.add_argument("--no-sandbox")  # Przydatne w środowiskach bez GUI
    # options.add_argument("--disable-dev-shm-usage")  # Ograniczenia pamięci współdzielonej

    # Inicjalizacja przeglądarki Chrome
    driver = webdriver.Chrome(driver_path, options=options)

    try:
        # Otwórz Google
        driver.get("https://www.google.com")

        # Poczekaj na załadowanie strony (opcjonalne, aby uniknąć problemów z ładowaniem)
        time.sleep(2)

        # Znajdź przycisk akceptacji cookies i kliknij
        try:
            accept_button = driver.find_element(By.XPATH, "//button[contains(., 'Zaakceptuj wszystko') or contains(., 'Accept all')]")
            accept_button.click()
            print("Zaakceptowano cookies.")
        except Exception as e:
            print("Nie znaleziono przycisku cookies lub wystąpił błąd:", e)

        # Znajdź pole wyszukiwania
        search_box = driver.find_element(By.NAME, "q")

        # Wpisz zapytanie i naciśnij Enter
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)

        # Poczekaj na załadowanie wyników
        time.sleep(2)

        # Pobierz linki z wyników wyszukiwania
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
        # Zamknij przeglądarkę
        driver.quit()

#search_query="Szpital psychiatryczny Millhaven, rok 1979. Okultystyczny rytuał kończy się katastrofą. Z szanowanej niegdyś rodziny ocalała tylko jedna osoba. Sprawę odłożono na półkę na dziesiątki lat do czasu"
# search_query="Buntownicy, gwiazdy, rewelucjoniści! Ashe, McEnroe, Borg, King, Navratilova, Evert na zawsze odmienili oblicze tenisa. Stali się legendami tego sportu, ale walczyli także poza kortem. Odważnie przekraczali granice i mieli odwagę zmieniać świat. Twórcy programu przedstawiają złotą erę tenisa przez pryzmat turnieju w Wimbledonie."

# google_search(search_query)
# exit()
