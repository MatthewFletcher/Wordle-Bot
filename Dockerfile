FROM python:3.8-slim-buster
COPY requirements.txt . 
RUN python3 -m pip install -f requirements.txt
COPY . .
CMD ["python3", "wordle.py"]
