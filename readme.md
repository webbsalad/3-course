основное задание выполнено полностью

дополнительное задание:
1, 2, 4  выполнены полностью
3 - приложение собирает только бизнесовые метрики

# инструкция по запуску:

## вариант 1 (без клонирования репозитория через docker hub):

#### **создание сети и контейнера с postgres(если хотите использовать свою бд то просто в дальнейшем ссылках на бд вставляйте свою):**
```
docker network create pvz-net

docker run -d \
  --name db \
  --network app-net \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=pvz-password \
  -e POSTGRES_DB=postgres \
  postgres:15-alpine

```

#### **пул и запуск контейнера c env параметрами:**
```
docker run -d --name pvz-app \
  --network pvz-net \
  -p 8080:8080 \
  -p 3000:3000 \
  -p 9000:9000
  -e DSN="postgres://postgres:pvz-password@pvz-db:5432/postgres?sslmode=disable" \
  -e JWT_SECRET="test secret" \
  docker.io/websalad/pvz:latest

```
- DSN - ваша бд (если делали бд по инструкции выше то можете оставить как есть если нет то замените DSN и уберитe параметр network)
- JWT_SECRET - секрет для генерации токенов

##  вариант 2 (с клонированием репозитория и запуском через docker compose):

#### **склонируйте репозиторий:**
```
git clone github.com/webbsalad/pvz
```

#### **в корне проекта создайте .env файл с наполнением вида:**
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=pvz-password
POSTGRES_DB=postgres

DSN=postgres://postgres:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}?sslmode=disable
JWT_SECRET=test secret
```

#### **выполните команду:**
```
docker-compose up --build
```


### вариант 3 (с клонированием репозитория и запуском через go run):

#### **создание сети и контейнера с postgres(если хотите использовать свою бд то просто в дальнейшем ссылках на бд вставляйте свою):**
```
docker network create pvz-net

docker run -d \
  --name db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=pvz-password \
  -e POSTGRES_DB=postgres \
  postgres:15-alpine
```

#### **склонируйте репозиторий:**
```
git clone github.com/webbsalad/pvz
```

#### **выполнение миграций:**
```
goose -dir migrations  postgres "postgres://postgres:pvz-password@localhost:5432/postgres?sslmode=disable" up
```

#### **запуск приложения:**
```
DSN="postgres://postgres:pvz-password@localhost:5432/postgres?sslmode=disable" \
JWT_SECRET="test secret" \
go run cmd/main.go -env=staging --log-file=./logs/app.log
```



 Примечание: для интеграционных тестов нужно создать файл .env.test
``` 
testDSN=postgres://postgres:test-pvz-password@localhost:5432/postgres?sslmode=disable
testJWT_SECRET=test secret
```