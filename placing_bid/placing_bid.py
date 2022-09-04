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
        # The output data must be presented by an implementation of the output boundary interface
        # The benefit is the output boundary is an argument to this use case.
        # So it allows other boundaries to be used without changing the use case code at all.
        self._output_boundary.present(
            PlacingBidOutputDto(is_winning=True, current_price=input_dto.amount)
        )


class PlacingBidWebPresenter(PlacingBidOutputBoundary):

    def present(self, output_dto: PlacingBidOutputDto) -> None:
        message = (
            f"Hooray! You are a winner"
            if output_dto.is_winning
            else f"Your bid is too low. Current price is {output_dto.current_price}"
        )
        # Currently output is in console. But will be a flask Response object in future
        print(f"message: {message}")


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
    use_case = PlacingBid(output_boundary)
    use_case.execute(input_dto)
    expected_output_dto = PlacingBidOutputDto(is_winning=True, current_price=price)
