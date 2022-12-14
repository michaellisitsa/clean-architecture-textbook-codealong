from flask import Blueprint, Response, abort, jsonify, make_response, request
import injector
import flask_injector
from flask_login import current_user

from auctions.application.use_cases.placing_bid import (
    PlacingBid,
    PlacingBidInputDto,
    PlacingBidOutputBoundary,
    PlacingBidWebPresenter,
)
from auctions.domain.value_objects import AuctionId
from web_app.web_app.serialization.dto import get_dto

auctions_blueprint = Blueprint("auctions_blueprint", __name__)


class AuctionsWeb(injector.Module):
    @injector.provider
    @flask_injector.request
    def placing_bid_output_boundary(
        self,
    ) -> PlacingBidOutputBoundary:
        return PlacingBidWebPresenter()


@auctions_blueprint.route("/<int:auction_id>/bids", methods=["POST"])
def place_bid(
    auction_id: AuctionId,
    placing_bid_uc: PlacingBid,
    presenter: PlacingBidOutputBoundary,
) -> Response:
    if not current_user.is_authenticated:
        abort(403)

    dto = get_dto(
        request,
        PlacingBidInputDto,
        context={"auction_id": auction_id, "bidder_id": current_user.id},
    )

    placing_bid_uc.execute(dto)
    return presenter.response  # type: ignore
