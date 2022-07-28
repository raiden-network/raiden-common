from raiden_common.transfer.architecture import Event
from raiden_common.transfer.channel import get_status
from raiden_common.transfer.events import ContractSendSecretReveal
from raiden_common.transfer.state import CHANNEL_STATES_UP_TO_CLOSED, NettingChannelState
from raiden_common.utils.typing import (
    BlockExpiration,
    BlockHash,
    List,
    Secret,
    T_Secret,
    typecheck,
)


def events_for_onchain_secretreveal(
    channel_state: NettingChannelState,
    secret: Secret,
    expiration: BlockExpiration,
    block_hash: BlockHash,
) -> List[Event]:
    events: List[Event] = []

    typecheck(secret, T_Secret)

    if get_status(channel_state) in CHANNEL_STATES_UP_TO_CLOSED:
        reveal_event = ContractSendSecretReveal(
            expiration=expiration, secret=secret, triggered_by_block_hash=block_hash
        )
        events.append(reveal_event)

    return events
