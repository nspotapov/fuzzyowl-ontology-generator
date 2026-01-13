FROM python:3.12.3-alpine

WORKDIR /usr/src/app

RUN --mount=type=bind,source=requirements.txt,target=requirements.txt \
    pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python3", "main.py"]
