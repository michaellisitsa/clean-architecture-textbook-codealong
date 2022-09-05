from bids.bid import Bid
from placing_bid.money import Money
from placing_bid.value_objects import AuctionId, BidderId


class Auction:
    def __init__(
        self, id: AuctionId, title: str, starting_price: Money, bids: list[Bid]
    ) -> None:
        self.id = id
        self.title = title
        self.starting_price = starting_price
        self.bids = sorted(bids, key=lambda bid: bid.amount)

    def place_bid(self, bidder_id: BidderId, amount: Money) -> None:
        # check if the amount is greater than the current highest price
        pass

    @property
    def current_price(self) -> Money:
        if not self.bids:
            return self.starting_price
        else:
            return self._highest_bid.amount

    @property
    def _highest_bid(self) -> Bid:
        return self.bids[-1]

    @property
    def winners(self) -> list[BidderId]:
        if not self.bids:
            return []
        return [self._highest_bid.bidder_id]
