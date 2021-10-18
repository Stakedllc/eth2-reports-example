# ETH2 Reports via Staked API

### Prerequisites

1. Staked API Key which has read access to provisioned validators.

### Steps

1. Download dependencies using pip: `pip install python-dotenv pandas simplejson`
2. Add your Staked API Key to the .env file.
3. Add the target network (mainnet, testnet) to the .env file.
4. Add the aggregation period (raw, daily) to the .env file.
5. Run `python generate_report.py`
