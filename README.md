запуск сервера, создать .env с полями
  EXPIRE_MINUTES = 111
  SECRET_KEY = secretkey
  ALGORITHM =HS256
  DB_PATH = postgresql+asyncpg://root:root@localhost/test
docker-compose build && docker-compose up
