# from ..placing_bid import *
import unittest
from unittest.mock import Mock
from auctions.auction import Auction, AuctionsRepository, InMemoryAuctionsRepository
from bids.bid import Bid
from placing_bid.currency import USD
from placing_bid.money import Money

from placing_bid.placing_bid import (
    PlacingBid,
    PlacingBidInputDto,
    PlacingBidOutputBoundary,
    PlacingBidOutputDto,
)


class PlacingBidTests(unittest.TestCase):
    FRESH_AUCTION_ID = 2

    def setUp(self) -> None:
        self.output_boundary_mock = Mock(spec_set=PlacingBidOutputBoundary)
        repo = self._create_repo_with_auction()
        self.use_case = PlacingBid(self.output_boundary_mock, repo)

    def _create_repo_with_auction(
        self,
    ) -> AuctionsRepository:
        repo = InMemoryAuctionsRepository()
        fresh_auction = Auction(
            id=self.FRESH_AUCTION_ID,
            title="socks",
            starting_price=Money(USD, "1.99"),
            bids=[],
        )
        repo.save(fresh_auction)
        return repo

    def test_presets_data_for_winning(self):
        price = Money(USD, "10.00")
        input_dto = PlacingBidInputDto(
            bidder_id=1,
            auction_id=2,
            amount=price,
        )
        self.use_case.execute(input_dto)
        expected_output_dto = PlacingBidOutputDto(is_winning=True, current_price=price)
        self.output_boundary_mock.present.assert_called_once_with(expected_output_dto)

    def test_should_get_back_saved_auction(
        self,
    ) -> None:
        bids = [Bid(id=1, bidder_id=1, amount=Money(USD, "15.99"))]
        auction = Auction(
            id=1, title="Awesome Book", starting_price=Money(USD, "9.99"), bids=bids
        )
        repo = InMemoryAuctionsRepository()
        repo.save(auction)
        print(f"auction: {auction}")
        assert repo.get(auction.id) == auction


if __name__ == "__main__":
    unittest.main()
