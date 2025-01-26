from datetime import datetime
import sqlite3
import time
import re

from search_google_selenium import google_search as fun1

def remove_square_brackets(text):
    return re.sub(r'\[.*?\]', '', text)

def truncate_movie_description(description):
    newline_index = description.find('\n')
    shortened = description[:newline_index] if newline_index != -1 else description
    return remove_square_brackets(shortened)

def find_movie(descr_id, synopsis):
    print(f"descr_id: {descr_id}")
    truncated_description = truncate_movie_description(synopsis)

    print(truncated_description)
    results = fun1("site:filmweb.pl "+truncated_description)

    if not results:
        return "-"

    result_links= []
    result_links = [
        link for link in results
        if link.startswith("https://www.filmweb.pl/") and link.endswith(str(descr_id))
    ]
    result_links = list(set(result_links))

    # for index, link in enumerate(result_links, start=1):
    #     print(f"{index}. {link}")

    result = "-"
    if len(result_links) == 1:
        result = result_links[0]

    return result

def update_database_with_links(conn, limit=1):
    """
    Aktualizuje bazę danych `movies`, wstawiając poprawne linki do `filmweb_url`.
    """
    cursor = conn.cursor()
    cursor.execute(f"SELECT descr_id, synopsis FROM movies WHERE filmweb_url = 'q' limit {limit}")
    rows = cursor.fetchall()

    for descr_id, synopsis in rows:
        result = find_movie(descr_id, synopsis)

        cursor.execute("UPDATE movies SET filmweb_url = ? WHERE descr_id = ?", (result, descr_id))
        conn.commit()
        print(f"Zaktualizowano rekord {descr_id} z wartością {result}")

def is_within_time_range(start_hour, end_hour):
    """
    Sprawdza, czy aktualna godzina mieści się w przedziale czasowym.
    """
    current_hour = datetime.now().hour
    return start_hour <= current_hour < end_hour

def main():
    """
    Główna funkcja skryptu, uruchamiana tylko w wyznaczonym czasie.
    """
    while True:
        if not is_within_time_range(1, 8):
            print("Poza dozwolonym przedziałem czasowym (1:00-8:00). Czekam...")
            time.sleep(120)
        else:
            print("Rozpoczynam działanie skryptu...")
            with sqlite3.connect('movies.db') as conn:
                update_database_with_links(conn)

def test():
    with sqlite3.connect('movies.db') as conn:
        update_database_with_links(conn)

if __name__ == "__main__":
    #main()
    test()
