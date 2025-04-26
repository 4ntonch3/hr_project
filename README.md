# Interview Project

## Работа с Docker

### Сборка

```sh
docker build -t interview_project .
```

### Запуск

Docker RUN:

```sh
docker run -it -d -p 8000:8000 --name interview_project interview_project
```

Docker-Compose:

```sh
docker-compose up -d
```
