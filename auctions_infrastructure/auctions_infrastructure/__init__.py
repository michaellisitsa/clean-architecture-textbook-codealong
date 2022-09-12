import injector
from auctions.application.repositories.auctions import AuctionsRepository
from auctions.domain.entities.auction import Auction
from auctions_infrastructure.auctions_infrastructure.repositories.in_memory_auctions_repository import (
    InMemoryAuctionsRepository,
)
from placing_bid.currency import USD
from placing_bid.money import Money


class AuctionsInfrastructure(injector.Module):
    @injector.provider
    def auctions_repo(
        self,
    ) -> AuctionsRepository:
        "provide an auctions repo to whoever needs it: e.g. InMemoryAuctionRepo"
        example_auction = Auction(
            id=1, title="Exemplary Auction", starting_price=Money(USD, "12.99"), bids=[]
        )
        repo = InMemoryAuctionsRepository()
        repo.save(example_auction)
        return repo
