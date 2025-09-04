FROM python:alpine3.22

# Устанавливаем компилятор и системные зависимости
RUN apk add --no-cache gcc musl-dev linux-headers

# Создание группы и пользователя в Alpine Linux
RUN addgroup -S groupdjango && adduser -S userdj -G groupdjango


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
WORKDIR /app/www/wallet_rest
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "manage.py", "loaddata", "wallet_wallet.json"]
USER userdj