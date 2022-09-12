import injector

from auctions import Auctions
from auctions_infrastructure.auctions_infrastructure import AuctionsInfrastructure


def setup_dependency_injection() -> injector.Injector:
    return injector.Injector(
        [Auctions(), AuctionsInfrastructure],
        auto_bind=False,
    )
