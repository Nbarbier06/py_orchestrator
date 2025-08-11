FROM python:3.11-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 1) Installer les deps une seule fois (couche Docker mise en cache)
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 2) Copier le code (modifs = rebuild léger, pas de réinstall complète)
COPY . .

EXPOSE 8088
CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8088"]
