from collections import defaultdict
from typing import List


class Event:
    def __init__(
        self,
        block_hash: str,
        block_number: int,
        transaction_hash: str,
        event_index: int,
        from_address: str,
        keys: List[str],
        data: List[str],
        timestamp: int,
        key_name: str,
    ):
        self.block_hash = block_hash
        self.block_number = block_number
        self.transaction_hash = transaction_hash
        self.event_index = event_index
        self.from_address = from_address
        self.keys = keys
        self.data = data
        self.timestamp = timestamp
        self.key_name = key_name

        self.user = self.data[0]
        self.token = self.data[1]

        if key_name in ["zklend::market::Market::Borrowing", "zklend::market::Market::Repay"]:
            self.face_amount = int(self.data[3], 16)

        if key_name in ["zklend::market::Market::Deposit", "zklend::market::Market::Withdrawal"]:
            self.face_amount = int(self.data[2], 16)

        self.asset = None

    @classmethod
    def from_json(cls, json_dict):
        return cls(**json_dict)

    def set_asset(self, asset):
        self.asset = asset


class Loan:

    def __init__(self, event: Event):
        self.deposits = defaultdict(int)
        self.borrowed = defaultdict(int)
        self.update_state(event=event)

    def update_state(self, event: Event):

        if event.key_name == "zklend::market::Market::Deposit":
            self.deposits[event.asset] += event.face_amount

        if event.key_name == "zklend::market::Market::Withdrawal":
            self.deposits[event.asset] -= event.face_amount

        if event.key_name == "zklend::market::Market::Borrowing":
            self.borrowed[event.asset] += event.face_amount

        if event.key_name == "zklend::market::Market::Repay":
            self.borrowed[event.asset] -= event.face_amount

    def health(self):
        # TODO implementation
        """ calculating health (will be in the zklend docs)"""
        pass

    def sum_state(self):
        prices = {
            "ETH": 2200,
            "wstETH": 2200,
            "USD": 40000,
            "BTC": 40000,
            "DAI": 1,
            "USDC": 1,
            "USDT": 1
        }

        deposit = 0
        borrowed = 0

        for asset in self.deposits:
            deposit += prices[asset] * self.deposits[asset]

        for asset in self.borrowed:
            borrowed += prices[asset] * self.borrowed[asset]

        return {
            "deposit": deposit,
            "borrowed": borrowed
        }

