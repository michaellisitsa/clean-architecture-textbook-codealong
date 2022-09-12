from dataclasses import dataclass
import abc
from auctions.application.repositories.auctions import AuctionsRepository
from auctions.domain.entities.auction import (
    Auction,
)
from auctions_infrastructure.auctions_infrastructure.repositories.in_memory_auctions_repository import (
    InMemoryAuctionsRepository,
)
from auctions.domain.entities.bid import Bid
from placing_bid.money import Money

from flask import Blueprint, Response, abort, jsonify, make_response, request

from auctions.domain.value_objects import AuctionId, BidderId
import attr


@dataclass(frozen=True)
class PlacingBidInputDto:
    bidder_id: BidderId
    auction_id: AuctionId
    amount: Money


@dataclass(frozen=True)
class PlacingBidOutputDto:
    is_winning: bool
    current_price: Money


class PlacingBidOutputBoundary(abc.ABC):
    @abc.abstractmethod
    def present(self, output_dto: PlacingBidOutputDto) -> None:
        pass


@attr.s(auto_attribs=True)
class PlacingBid:
    _output_boundary: PlacingBidOutputBoundary
    _auctions_repo: AuctionsRepository

    def execute(self, input_dto: PlacingBidInputDto) -> None:
        auction = self._auctions_repo.get(input_dto.auction_id)
        auction.place_bid(
            bidder_id=input_dto.bidder_id,
            amount=input_dto.amount,
        )
        self._auctions_repo.save(auction)
        output_dto = PlacingBidOutputDto(
            is_winning=input_dto.bidder_id in auction.winners,
            current_price=auction.current_price,
        )
        # The output data must be presented by an implementation of the output boundary interface
        # The benefit is the output boundary is an argument to this use case.
        # So it allows other boundaries to be used without changing the use case code at all.
        self._output_boundary.present(output_dto=output_dto)


class PlacingBidWebPresenter(PlacingBidOutputBoundary):
    # Uncomment when presenting Flask response object
    response: Response

    def present(self, output_dto: PlacingBidOutputDto) -> None:
        message = (
            f"Hooray! You are a winner"
            if output_dto.is_winning
            else f"Your bid is too low. Current price is {output_dto.current_price}"
        )
        self.response = make_response(jsonify({"message": message}))


if __name__ == "__main__":
    # sample code for debugging purposes
    from placing_bid.currency import USD

    price = Money(USD, "10.00")
    input_dto = PlacingBidInputDto(
        bidder_id=1,
        auction_id=2,
        amount=price,
    )
    output_boundary = PlacingBidWebPresenter()

    def _create_repo_with_auction() -> AuctionsRepository:
        repo = InMemoryAuctionsRepository()
        fresh_auction = Auction(
            id=2,
            title="socks",
            starting_price=Money(USD, "1.99"),
            bids=[],
        )
        repo.save(fresh_auction)
        second_auction = Auction(
            id=3,
            title="underwear",
            starting_price=Money(USD, "2.99"),
            bids=[],
        )
        repo.save(second_auction)
        return repo

    use_case = PlacingBid(output_boundary, _create_repo_with_auction())
    use_case.execute(input_dto)
    # expected_output_dto = PlacingBidOutputDto(is_winning=True, current_price=price)

    bids = [Bid(id=1, bidder_id=1, amount=Money(USD, "15.99"))]
    auction = Auction(
        id=1, title="Awesome Book", starting_price=Money(USD, "9.99"), bids=bids
    )
    repo = InMemoryAuctionsRepository()
    repo.save(auction)
    print(f"auction: {auction}")
    print(f"repo get: {repo.get(auction.id)}")
