FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY noshow ./noshow
RUN python -m noshow.train
ENV PORT=8080
CMD ["sh", "-c", "uvicorn noshow.api:app --host 0.0.0.0 --port ${PORT}"]
