import requests


PRICES = {
    "ETH": 2200,
    "wstETH": 2200,
    "USD": 40000,
    "BTC": 40000,
    "DAI": 1,
    "USDC": 1,
    "USDT": 1
}


class Loan:

    def update_state(self):
        # TODO implementation
        """update based on deposit, withdraw, borrow and repay"""
        pass

    def health(self):
        # TODO implementation
        """ calculating health (will be in the zklend docs)"""
        pass


def fetch_events():
    """Fetch all data just by using pagination, next_url in response"""
    url = "https://api.starkscan.co/api/v0/events?from_address=0x04c0a5193d58f74fbace4b74dcf65481e734ed1714121bdc571da345540efa05"

    headers = {
        "accept": "application/json",
        "x-api-key": "docs-starkscan-co-api-3"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get('data', [])


if __name__ == '__main__':
    print(fetch_events())
