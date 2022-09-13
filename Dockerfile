FROM python:3.8-slim-buster
COPY requirements.txt . 
COPY data .
RUN python3 -m pip install -r requirements.txt
COPY . .
CMD ["python3", "wordle.py"]
