# 베이스 이미지 명시
FROM python:3.11
ENV PORT 8000
WORKDIR /app

RUN pip install fastapi uvicorn genai ibm-generative-ai LangChain
COPY . . 

EXPOSE $PORT

CMD uvicorn --host=0.0.0.0 --port $PORT  main:app


