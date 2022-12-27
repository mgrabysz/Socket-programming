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