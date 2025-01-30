### Baza danych filmweb

Mając zbiór opisów filmów należy odnaleźć przyporządkowanie do nich łącza url, z którego moża wydobyć informacje takie jak tytuł, rok publikacji oraz id. W tym celu użyto skryptu python korzystającego z selenium i wyszukiwarki google.

### Testy
Mając bazę testową `test_movies.db` wywołać `python3 main.py`. Wyniki można przeglądać w aplikacji flask uruchamianej `webapp./web.py` pod adresem `localhost:8080`

### Zapytania SQL

## wybierz filmy, które jeszcze nie mają znalezionego url
`
SELECT descr_id, id, synopsis, filmweb_url
FROM movies where filmweb_url is null;
`

## wybierz ile jest filmów bez znalezionego url
`
SELECT count(*)
FROM movies where filmweb_url is null;
`

## wybierz film po id
`
SELECT descr_id, id, synopsis, filmweb_url
FROM movies where descr_id=10041311;
`

### Komendy sqlite

## zapis backupu do pliku
sqlite3 movies.db .dump > ./backup/movies_backup_$(date +"%Y-%m-%d_%H-%M-%S").sql

## utworzenie nowej bazy z backupu
sqlite3 movies.db < ./backup/movies_backup.sql

## tworzenie bazy testowej z bazy głównej
sqlite3 test_movies.db <<EOF
ATTACH 'movies.db' AS old_db;
CREATE TABLE movies AS SELECT * FROM old_db.movies order by descr_id limit 1000;
DETACH old_db;
EOF



