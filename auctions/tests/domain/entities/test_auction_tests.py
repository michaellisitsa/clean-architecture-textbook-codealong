import unittest
from bids.bid import Bid
from placing_bid.currency import USD
from placing_bid.money import Money

from auctions.domain.entities.auction import Auction


class AuctionTests(unittest.TestCase):
    def test_untouched_auction_has_current_price_equal_to_starting(self):
        starting_price = Money(USD, "12.99")
        auction = Auction(
            id=1,
            title="Auction",
            starting_price=starting_price,
            bids=[],
        )

        assert starting_price == auction.current_price

    def test_highest_bid_returned(self):
        starting_price = Money(USD, "12.99")
        bid1 = Bid(id=1, bidder_id=1, amount=Money(USD, "19.99"))
        bid2 = Bid(id=1, bidder_id=1, amount=Money(USD, "15.99"))
        auction = Auction(
            id=1,
            title="Auction",
            starting_price=starting_price,
            bids=[bid1, bid2],
        )

        assert auction.current_price == bid1.amount


if __name__ == "__main__":
    unittest.main()
