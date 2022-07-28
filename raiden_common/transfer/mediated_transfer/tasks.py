from dataclasses import dataclass, field
from typing import ClassVar

from raiden_common.transfer.architecture import TransferRole, TransferTask
from raiden_common.transfer.identifiers import CanonicalIdentifier
from raiden_common.transfer.mediated_transfer.state import (
    InitiatorPaymentState,
    MediatorTransferState,
    TargetTransferState,
)
from raiden_common.utils.typing import ChannelID, TokenNetworkAddress


@dataclass
class InitiatorTask(TransferTask):
    role: ClassVar[TransferRole] = TransferRole.INITIATOR

    manager_state: InitiatorPaymentState = field(repr=False)


@dataclass
class MediatorTask(TransferTask):
    role: ClassVar[TransferRole] = TransferRole.MEDIATOR

    mediator_state: MediatorTransferState = field(repr=False)


@dataclass
class TargetTask(TransferTask):
    role: ClassVar[TransferRole] = TransferRole.TARGET

    token_network_address: TokenNetworkAddress = field(init=False, repr=False)
    canonical_identifier: CanonicalIdentifier
    target_state: TargetTransferState = field(repr=False)

    def __post_init__(self) -> None:
        # Mypy does not allow overringing the `token_network_address` field
        # with a property, right now (see
        # https://github.com/python/mypy/issues/4125). So we use this
        # combination of `init=False` and `__post_init__`.
        self.token_network_address = self.canonical_identifier.token_network_address

    @property
    def channel_identifier(self) -> ChannelID:
        return self.canonical_identifier.channel_identifier
