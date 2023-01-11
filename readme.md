# Programowanie sieciowe
Patrycja Wysocka, Szymon Wysocki, Jan Jedrzejewski, Marcin Grabysz

Realizacja: zima 2022

Opiekun projeku: Jacek Wytrębowicz

## Projekt

### Klient
Funkcjonalność symulowania urządzeń wysyłających dane do bramy jest zaimplementowana w module `client.py`. Manager klientów tworzy zadaną liczbę klientów w sposób współbieżny, z których każdy wysyła kolejno: wiadomość rejestracji, pewną liczbę wiadomości transmitujących dane, wiadomość wyrejestrowania.

Moduł można wywołać z opcjonalnymi argumentami
```shell
usage: client.py [-h] [-a ADDRESS] [-p PORT] [-d DEVICES] [-m MESSAGES] [-i INTERVAL]
```
Można też bez; wtedy program uruchomi się z argumentami domyślnymi

### Brama komunikacyjna
Podstawowy moduł projektu, odpowiada za agregację i przesyłąnie danych od Klientów do Serwerów. Pracuje na dwóch wątkach, jeden odbiera wiadomości drugi w określonych interwałach czasowych wysyła dane. Moduł `gateway.py` obsługuje funkcjonalność odbierania danych, w osobnych plikach `registration.py` oraz `transmission.py` obsługujemy odpowiednio prośby zarejestrowania i wyrejestrowania klientów, oraz otrzymane dane.

Moduł można uruchomić ze zdefiniowanymi parametrami lub bez nich. 
```shell
gateway.py [-a ADDRESS] [-p PORT] [-i INTERVAL] [-k KEY] [-v]
```
Domyśle wartości są kompatybilne z domyślnymi wartościami klientów i serwerów.

Opcjonalny argument `KEY` to scieżka do klucza prywatnego w formacie .pem, na podstawie którego generowane będą podpisy cyfrowe pod przesłanymi wiadomościami. Nie podanie tego argumentu spowoduje wygenerowanie nowego klucza przy uruchomieniu bramy i zapisanie go w pliku `key.pem`

Uruchomienie bramy z argumentem `-v` (verbose) spowoduje wyświetlanie w konsoli całego cyfrowego podpisu każdej wiadomości (ciąg 256 bajtów). Domyślnie na wyjściu standardowym pojawia się tylko początkowy fragment.
### Budowanie kontenerów

```bash
docker compose build
```

### Uruchamianie przykładowej konfiguracji (3 urządzenia + brama + 2 serwery)

```bash
docker compose up [-d]
```

### Monitorowanie logów

```bash
docker compose logs --follow [nazwy kontenerów]
```
