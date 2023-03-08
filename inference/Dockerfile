FROM python:3.8-slim

COPY PostPartumInference.py /app/PostPartumInference.py
COPY  rf.pkl /app/rf.pkl

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install -r requirements.txt

ADD PostPartumInference.py .

ADD rf.pkl .


CMD ["python3", "PostPartumInference.py"]



# COPY --from=btc_pandas /app/dummy.csv /Users/hakymulla/Documents/Files/bacalhau/bitcoin_trading/results/
#  docker buildx build --platform linux/amd64 --push -t hakymulla/postpartum:ml . 

# bacalhau docker run --id-only --cpu 1 hakymulla/postpartum:inference -- python PostPartumInference.py  --ag 30 --t "Yes" --i "Yes" --n "Yes" --c "Yes" --l "Maybe" --g "Yes" --b "Yes" --s "Yes" 

# bacalhau docker run --id-only --cpu 1 hakymulla/postpartum:inferenc -- python PostPartumInference.py --o ./outputs

# bacalhau list --id-filter 389c63fe-8ad4-4ce6-8373-c6186bff71b6
# bacalhau describe 21b76944-7dd1-46cc-9f05-9c98ae326d42
# bacalhau get d36f2b7f-4946-4a13-81c4-7cdacd2e8bf3