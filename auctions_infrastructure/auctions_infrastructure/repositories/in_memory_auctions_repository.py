import copy
from auctions.application.repositories.auctions import AuctionsRepository
from auctions.domain.entities.auction import Auction
from placing_bid.value_objects import AuctionId


class InMemoryAuctionsRepository(AuctionsRepository):
    def __init__(self) -> None:
        self._storage: dict[AuctionId, Auction] = {}

    def get(self, auction_id: AuctionId) -> Auction:
        return copy.deepcopy(self._storage[auction_id])

    def save(self, auction: Auction) -> None:
        self._storage[auction.id] = copy.deepcopy(auction)
