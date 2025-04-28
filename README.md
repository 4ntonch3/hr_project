# Interview Project

## Поднимаем базу

```sh
docker-compose -f docker-compose.yml up -d
```

## Устанавливаем зависимости

```sh
pip install -r requirements.txt 
```

## Запуск тестов
```sh
pytest tests/
```

## Запуск линтеров
```sh
pre-commit install # при первом запуске
pre-commit run --all-files
```
