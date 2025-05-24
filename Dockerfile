FROM python:3.11-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends tzdata \
 && ln -fs /usr/share/zoneinfo/Europe/Riga /etc/localtime \
 && dpkg-reconfigure -f noninteractive tzdata \
 && rm -rf /var/lib/apt/lists/*

ENV TZ=Europe/Riga

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
