# Semantive

## Konfiguracja

Poniższe instrukcje służą przygotowaniu środowiska pod aplikację oraz uruchamianiu serwera

## Wymagania

Wymagany jest python w wersji >=3.3

## Setup

1. Sklonuj repozytorium `git clone https://github.com/lampo100/semantive.git`
2. Wywołaj `make setup` w głównym folderze projektu

## Uruchamianie serwera

Po skonfigurowaniu środowiska serwer może zostać uruchomiony poprzez wywołanie. 
`make serve [HOST=<adres>] [PORT=<port>]` 
Domyślnie serwis dostępny jest pod adresem 127.0.0.1:5000

## Testowanie

W celu uruchomienia testów należy wywołać 
`make test`

## Design API

Opis API dostępny jest pod adresem 
https://app.swaggerhub.com/apis-docs/lampo1002/Semantive/v1

## Decyzje przy projektowaniu

W serwisie wydzieliłem 3 podstawowe zasoby:
* ScrapingTask
* Image
* Text

### Tworzenie nowego zadania

Proces tworzenia nowego zadania pobrania danych wygląda następująco:
1. Użytkownik zleca stworzenie nowego zadania podając adres strony, to czy ma być pobierany tekst czy obrazy oraz opcjonalnie czy pobrane dane mają jakiś tag(np. "pies", "kot", "sport").
2. Tworzone jest nowe zadanie o podanych parametrach i przekazany jest adres pod którym użytkownik może sprawdzać jego status.

Dane pobrane ze stron dostępne są pod odpowiednimi adresami. Mogą być one przefiltrowane używając adresu strony z której były pobrane, lub też z pomocą opcjonalnego tagu. Dodanie go wydaje mi się sensownym dodatkiem, ponieważ przy uczeniu maszynowym bardziej niż to z jakiej strony pobrane były zdjęcia/tekst, przyda nam się informacja o tym do jakiej kategorii należą. 
Nie chciałem jednakże pozbawiać użytkownika możliwości sprawdzania danych z określonej strony, dlatego też dostępne są obie opcje.

Możliwa jest także próba automatycznego kategoryzowania obrazków, np. dzięki atrybutom `alt`. Musimy się liczyć z tym, że nie wszystkie obrazki będo go miały lub że będą one błędnie oznaczone.

Przy ewentualnym rozbudowaniu systemu należałoby prawdopodobnie wprowadzić nieco bardziej skomplikowany system kategoryzacji zebranych danych.

### Kolekcje

W celu przejrzenia wszystkich zadań/obrazów/tekstów w systemie użytkownik może wysłać zapytanie z użyciem metody GET na odpowieni adres.

Zwrócone zostaną dane w formacie application/hal+json. Przykładowa kolejkcja zadań:
```json
{
  "size": 2,
  "page": 2,
  "total": 1234,
  "_embedded": {
    "tasks": [
      {
        "_links": {
          "self": {
            "href": "/api/scraping-tasks/33"
          }
        },
        "id": 33,
        "source": "https://stockimages.com/some/page",
        "active": true
      },
      {
        "_links": {
          "self": {
            "href": "/api/scraping-tasks/35"
          }
        },
        "id": 35,
        "source": "https://otherstocks.com/some/page",
        "active": false
      }
    ]
  }
}
```
Użyłem konwencji hal w celu ujednolicenia sposobu zwracania kolekcji w systemie. 

### Przechowywanie obrazów i tekstu

Pod adresem `/api/images/{id}` dostępne są metadane przechowywanego obrazu o podanym id. Sam obraz dostępny jest pod adresem `/api/images/{id}/content`. 
Rozdzielenie to wydaje mi się korzystne ze względu na to że jesteśmy w stanie przesyłać oddzielnie informacje o obrazku a oddzielnie sam obrazek. 
Dla zachowania konwencji teksty dostępne są w identyczny sposób.

W prototypie do przechowywania użyłbym bazy danych sqlite.

### Asynchroniczność zadań

Jako że pobieranie ze strony obrazów może trwać bardzo długo, zadania powinny być obsługiwane przez zupełnie inny proces/wątek niż ten który obsługuje mikroserwis. Inaczej mogłoby dojść do zablokowania wszystkich wątków/procesów i tym samym zablokowanie mikroserwisu.

Proponowanym przeze mnie rozwiązaniem jest użycie `Celery` (http://www.celeryproject.org/) w celu postawienia serwera roboczego który zajmować się będzie wykonywaniem zleconych zadań i pobieraniem danych.
Jest to oczywiście jedno z wielu możliwych rozwiązań.

### Implementacja mikroserwisu

Z uwagi na mały rozmiar serwisu, postanowiłem zamiast bardziej znajomej mi opcji w stylu `Django`, użyć lekkiego frameworku typu `Flask`. Wydaje mi się on wystarczający do implementacji serwisu tej wielkości, i zdecydowanie przyspieszył prototypowanie.

Ponadto jako serwer HTTP postanowiłem użyć `gunicorn` z uwagi na jego prostotę użycia, szybkość i małe zużycie zasobów.

### Konfiguracja serwisu

Konfigurację serwisu i automatyzację uruchamiania go postanowiłem wprowadzić używając `venv` oraz programu `make`.

Prawdopodobnie lepszą opcją byłoby użycie Dockera, jednakże z uwagi na mój brak doświadczenia pracy z nim, postanowiłem użyć tutaj nieco prostszego rozwiązania.

### Testy

Do testowania postanowiłem wybrać znajomy mi pakiet `unittest`. Testy odpalane są z użyciem polecenia `make test`


### Data scraping

Przy szukaniu odpowiedniego rozwiązania tego problemu natknąłem się na framework `Scrapy`. Szybkie przeczytanie wstępu dokumentacji pozwoliło mi stwierdzić że byłby on zdecydowanie wystarczający przy problemie pobierania tekstu i statycznych zasobów.
Jeżeli preferowane byłoby "lżejsze" rozwiązanie, to alternatywą może być użycie `Beautiful Soup` jednakże użycie tej biblioteki wymagałoby minimalnie większej ilości kodu niż użycie Scrapiego.

Ogólnie wydaje mi się że efektywny data scraping to dosyć złożony problem i wymagałby głębszego przemyślenia i dopasowania rozwiązania do konkretnych stron.


## Podsumowanie

Serwis stworzony w wyżej opisany sposób powinien dosyć dobrze obsługiwać dużą ilość zapytań. Poszczególne komponenty systemu są odpowiednio rozdzielone i niezależne od siebie, dlatego też łatwo byłoby wprowadzić poprawki/zmiany.

Aktualnie wydaje mi się że wraz ze wzrostem danych przydałaby się lepsza ich organizacja, niż samo filtrowanie po "opcjonalnym" tagu albo po stronie z której pochodzą. Najlepiej byłoby użyć odpowiednio zaprojektowanej

W przypadku rozszerzenia możliwości serwisu, dobrą decyzją byłoby zapewne użycie odpowiednio zaprojektowanej bazy danych na oddzielnym serwerze. 
