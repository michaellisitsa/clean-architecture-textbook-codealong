from dataclasses import dataclass
from placing_bid.money import Money
from auctions.domain.value_objects import AuctionId, BidId, BidderId


@dataclass
class Bid:
    id: BidId | None
    bidder_id: BidderId
    amount: Money
