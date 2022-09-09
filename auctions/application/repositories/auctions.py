import abc
from auctions.domain.entities.auction import Auction
from auctions.domain.value_objects import AuctionId


class AuctionsRepository(abc.ABC):
    """
    Data access Interface (Abstract Repository).
    Allows the use case to fetch the Entitity and persist it afterwards.
    """

    @abc.abstractmethod
    def get(self, auction_id: AuctionId) -> Auction:
        pass

    @abc.abstractmethod
    def save(self, auction: Auction) -> None:
        pass
