import os
from dotenv import load_dotenv
from datetime import datetime
import requests
import pandas as pd
import simplejson

load_dotenv()

STAKED_API_KEY = os.getenv('STAKED_API_KEY')
NETWORK = os.getenv('NETWORK')
AGGREGATION_PERIOD = os.getenv('AGGREGATION_PERIOD')

url = f"https://{NETWORK}.staked.cloud/api/reports/eth2.0"


def get_transactions():
    path = "/txns"
    params = {
        "api_key": STAKED_API_KEY
    }
    response = requests.get(url + path, params)
    return response.json()


def aggregate_transactions(transactions):
    if AGGREGATION_PERIOD == "daily":
        data = []
        daily_data = {}
        for transaction in transactions:
            transaction = clean_transaction(transaction)
            date = str(datetime.fromisoformat(transaction["timestamp"]).date())
            kind = transaction["kind"]
            if date in daily_data:
                if kind in daily_data[date]:
                    daily_data[date][kind] += transaction["amount"]
                else:
                    daily_data[date][kind] = transaction["amount"]
            else:
                daily_data[date] = {}
                daily_data[date][kind] = transaction["amount"]
        for key in daily_data:
            reward = 0
            if "reward" in daily_data[key]:
                reward = daily_data[key]["reward"]
            delegation = 0
            if "delegation" in daily_data[key]:
                delegation = daily_data[key]["delegation"]
            data.append({
                "timestamp": key,
                "delegation": delegation,
                "reward": reward,
            })
        return data
    else:
        return list(map(clean_transaction, transactions))


def clean_transaction(transaction):
    return {
        "timestamp": transaction["transaction_time"],
        "kind": "delegation" if transaction["kind"] == "STK" else "reward",
        "validator_pubkey": transaction["holding_address"],
        "amount": transaction["total"] / 1e18,
    }


def convert_to_csv(data):
    pd.io.json._json.loads = lambda s, *a, **kw: simplejson.loads(s)
    df = pd.json_normalize(data)
    df.to_csv('./reports/data.csv', index=None)


def generate_report():
    report_data = aggregate_transactions(get_transactions())
    convert_to_csv(report_data)


generate_report()
