import injector
from auctions.application.repositories.auctions import AuctionsRepository

from auctions.application.use_cases.placing_bid import (
    PlacingBid,
    PlacingBidOutputBoundary,
)

__all__ = [
    # module
    "Auctions",
    # repositories
    "AuctionsRepository",
    # types
    "AuctionId",
    # use cases
    "PlacingBid",  # no input boundaries
    "PlacingBidInputDto",
    "PlacingBidOutputBoundary",
    "PlacingBidOutputDto",
]


class Auctions(injector.Module):
    @injector.provider
    def placing_bid_uc(
        self, boundary: PlacingBidOutputBoundary, repo: AuctionsRepository
    ) -> PlacingBid:
        return PlacingBid(boundary, repo)
