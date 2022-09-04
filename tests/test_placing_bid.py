# from ..placing_bid import *
import unittest
from unittest.mock import Mock
from placing_bid.currency import USD
from placing_bid.money import Money

from placing_bid.placing_bid import (
    PlacingBid,
    PlacingBidInputDto,
    PlacingBidOutputBoundary,
    PlacingBidOutputDto,
)


class PlacingBidTests(unittest.TestCase):
    def setUp(self) -> None:
        self.output_boundary_mock = Mock(spec_set=PlacingBidOutputBoundary)
        self.use_case = PlacingBid(self.output_boundary_mock)

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


if __name__ == "__main__":
    unittest.main()
