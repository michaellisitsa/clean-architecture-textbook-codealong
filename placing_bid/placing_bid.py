from dataclasses import dataclass
import abc
from placing_bid.money import Money

from placing_bid.value_objects import AuctionId, BidderId


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


class PlacingBid:
    def __init__(
        self,
        output_boundary: PlacingBidOutputBoundary,
    ) -> None:
        self._output_boundary = output_boundary

    def execute(self, input_dto: PlacingBidInputDto) -> None:
        self._output_boundary.present(
            PlacingBidOutputDto(is_winning=True, current_price=input_dto.amount)
        )
