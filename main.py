import requests
from typing import List

from models import Event, Loan


class StartScanSDK:
    def __init__(self, contract_address: str):
        self.contract_address = contract_address
        self.events: List[Event] = list()
        self.state_of_loans = dict()
        self.assets = {}
        self.asset_tokens = set()

    def fetch_events(self):
        """Fetch all data just by using pagination, next_url in response
        put limit 100 to work with more data
        """
        url = f"https://api.starkscan.co/api/v0/events?from_address={self.contract_address}&limit=100"

        headers = {
            "accept": "application/json",
            "x-api-key": "docs-starkscan-co-api-3"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            res = response.json().get('data', [])

            for item in res:
                if item.get('key_name') in [
                    "zklend::market::Market::Borrowing", "zklend::market::Market::Repay",
                    "zklend::market::Market::Deposit", "zklend::market::Market::Withdrawal"
                ]:
                    event = Event.from_json(item)
                    self.events.append(event)

                    self.asset_tokens.add(event.token)
        else:
            raise Exception("Something went wrong")

        for token in self.asset_tokens:
            self.get_asset(token)

        for event in self.events:
            event.set_asset(
                self.assets[event.token]
            )

    def get_asset(self, token):
        url = f"https://api.starkscan.co/api/v0/contract/{token}"

        headers = {
            "accept": "application/json",
            "x-api-key": "docs-starkscan-co-api-3"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            self.assets[token] = response.json()['name_tag'].split(" ")[1]
        else:
            raise Exception("alksdla")

    def build_loans(self):

        for event in self.events:

            if event.user in self.state_of_loans:
                self.state_of_loans[event.user].update_state(event=event)
            else:
                self.state_of_loans[event.user] = Loan(event=event)


if __name__ == '__main__':
    sdk = StartScanSDK(contract_address="0x04c0a5193d58f74fbace4b74dcf65481e734ed1714121bdc571da345540efa05")
    sdk.fetch_events()
    sdk.build_loans()

    for loan in sdk.state_of_loans:
        print(f"""
        Loan {loan} :
        State in $: {sdk.state_of_loans[loan].sum_state()}
        State per asset: 
            Deposit - {dict(sdk.state_of_loans[loan].deposits)} 
            Borrowed - {dict(sdk.state_of_loans[loan].borrowed)}
        
        Health: {sdk.state_of_loans[loan].health()}
        """)

