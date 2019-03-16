# Semantive

## Konfiguracja

Poniższe instrukcje służą przygotowaniu środowiska pod aplikację oraz uruchamianiu serwera

## Wymagania

Do uruchomienia serwisu potrzebny jest docker oraz docker-compose

## Setup

1. Sklonuj repozytorium `git clone https://github.com/lampo100/semantive.git`
2. Przejdź do sklonowanego folderu `cd semantive`
2. Wywołaj `sudo docker-compose up build` w głównym folderze projektu
Domyślnie serwis dostępny jest pod adresem 127.0.0.1:5000

## Testowanie

Testy uruchamiane są automatycznie przed postawieniem środowiska. Możliwe jest także wywołanie ich ręcznie z użyciem komendy `pytest`

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
Aktualnie jako message broker w celu komunikacji z workerem używany jest redis.

### Implementacja mikroserwisu

Z uwagi na mały rozmiar serwisu, postanowiłem zamiast bardziej znajomej mi opcji w stylu `Django`, użyć lekkiego frameworku typu `Flask`. Wydaje mi się on wystarczający do implementacji serwisu tej wielkości, i zdecydowanie przyspieszył prototypowanie.

Ponadto jako serwer HTTP postanowiłem użyć `gunicorn` z uwagi na jego prostotę użycia, szybkość i małe zużycie zasobów.

### Konfiguracja serwisu

Wstępnie konfigurację serwisu i automatyzację uruchamiania go postanowiłem wprowadzić używając `venv` oraz programu `make`.
Pod koniec stwierdziłem jednakże, że lepszym rozwiązaniem może być jednakże użycie dockera, dlatego też w wersji końcowej używam właśnie tego rozwiązania.

### Testy

Wstępnie do testów użyłem znajomego mi pakietu unittest, jednakże po wstępnym zapoznaniu się z pytest, doszedłem do wniosku, że jest on zdecydowanie lepszy ze względu na łatwość modularyzacji testów i możliwości ponownego użycia ich.

### Data scraping

Do data scrapingu postanowiłem użyć lekkiego pakietu BeautifulSoup4. Aktualnie zaimplementowany jest dosyć prosty sposób scrapowania. W przypadku tekstu usuwane są wszystkie tagi html a powstałe teksty sklejane są ze sobą w jeden dokument.
W przypadku obrazków znajdywane są wszystkie tagi `img` i z atrybutu `src` wyciągane są wszystkie adresy. Następnie w adresie znalezione zostanie jedno z szukanych rozszerzeń obrazów (np. png) obraz jest pobierany oraz zapisywany do bazy danych.

## Podsumowanie

Serwis stworzony w wyżej opisany sposób powinien dosyć dobrze obsługiwać dużą ilość zapytań. Poszczególne komponenty systemu są odpowiednio rozdzielone i niezależne od siebie, dlatego też łatwo byłoby wprowadzić poprawki/zmiany.

Aktualnie wydaje mi się że wraz ze wzrostem danych przydałaby się lepsza ich organizacja, niż samo filtrowanie po "opcjonalnym" tagu albo po stronie z której pochodzą.

Dodatkowym mankamentem jes

W przypadku rozszerzenia możliwości serwisu, dobrą decyzją byłoby zapewne użycie odpowiednio zaprojektowanej bazy danych na oddzielnym serwerze. 