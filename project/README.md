# Projekt PSI 22Z

Marcin Grabysz, Jan Jędrzejewski, Patrycja Wysocka, Szymon Wysocki

## Budowanie kontenerów

```bash
docker compose build
```

## Uruchamianie przykładowej konfiguracji (3 urządzenia + brama + 2 serwery)

```bash
docker compose up [-d]
```

## Monitorowanie logów

```bash
docker logs --follow [nazwy kontenerów]
```