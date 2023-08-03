# 베이스 이미지 명시
FROM python:3.11
ENV PORT 8000
WORKDIR /app

ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && cat /usr/local/lib/python3.11/site-packages/genai/extensions/langchain/__init__.py
COPY . . 

EXPOSE $PORT

CMD uvicorn --host=0.0.0.0 --port $PORT  main:app


