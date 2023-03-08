FROM python:3.8-slim

COPY PostPartum.py /app/PostPartum.py

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install -r requirements.txt

ADD PostPartum.py .

CMD ["python3", "PostPartum.py", "/inputs", "/outputs"]



# COPY --from=btc_pandas /app/dummy.csv /Users/hakymulla/Documents/Files/bacalhau/bitcoin_trading/results/