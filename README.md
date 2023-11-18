# Cadastre middleware

### Описание

Веб-приложение для кадастровой службы.

### Стэк технологий
  
- Backend - Flask.
  
- ORM - SQLAlchemy

- Database - PostgreDB.

### Как запустить проект:

Клонировать репозиторий:

```
git clone git@github.com:srj-lex/Cadastre-middleware.git
```
Перейти в директорию с проекта:
```
cd Cadastre-middleware
```
Переименовать .env_example в .env, при необходимости, внести изменения.

Запустить проект:
```
docker compose up
```

### Документация к API

Для получения описания существующих эндпоинтов перейдите

на http://localhost:5000/swagger/.

### Админка

Админка доступна по адресу http://localhost:5000/admin/.
