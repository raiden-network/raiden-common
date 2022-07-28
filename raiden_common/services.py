import structlog

from raiden_common.constants import (
    BLOCK_ID_LATEST,
    DAI_TOKEN_ADDRESS,
    WETH_TOKEN_ADDRESS,
    DeviceIDs,
    Environment,
    RoutingMode,
)
from raiden_common.messages.monitoring_service import RequestMonitoring
from raiden_common.messages.path_finding_service import PFSCapacityUpdate, PFSFeeUpdate
from raiden_common.settings import (
    MIN_MONITORING_AMOUNT_DAI,
    MIN_MONITORING_AMOUNT_WETH,
    MONITORING_REWARD,
)
from raiden_common.transfer import views
from raiden_common.transfer.architecture import BalanceProofSignedState
from raiden_common.transfer.channel import get_balance
from raiden_common.transfer.identifiers import CanonicalIdentifier
from raiden_common.transfer.state import ChainState
from raiden_common.utils.formatting import to_checksum_address
from raiden_common.utils.transfers import to_rdn
from raiden_common.utils.typing import TYPE_CHECKING, Address

if TYPE_CHECKING:
    from raiden_common.raiden_service import RaidenService


log = structlog.get_logger(__name__)


def send_pfs_update(
    raiden: "RaidenService",
    canonical_identifier: CanonicalIdentifier,
    update_fee_schedule: bool = False,
) -> None:
    if raiden.routing_mode == RoutingMode.PRIVATE:
        return

    channel_state = views.get_channelstate_by_canonical_identifier(
        chain_state=views.state_from_raiden(raiden), canonical_identifier=canonical_identifier
    )

    if channel_state is None:
        return

    capacity_msg = PFSCapacityUpdate.from_channel_state(channel_state)
    capacity_msg.sign(raiden.signer)
    raiden.transport.broadcast(capacity_msg, device_id=DeviceIDs.PFS)
    log.debug(
        "Sent a PFS Capacity Update",
        node=to_checksum_address(raiden.address),
        message=capacity_msg,
        channel_state=channel_state,
    )

    if update_fee_schedule:
        fee_msg = PFSFeeUpdate.from_channel_state(channel_state)
        fee_msg.sign(raiden.signer)

        raiden.transport.broadcast(fee_msg, device_id=DeviceIDs.PFS)
        log.debug(
            "Sent a PFS Fee Update",
            node=to_checksum_address(raiden.address),
            message=fee_msg,
            channel_state=channel_state,
        )


def update_monitoring_service_from_balance_proof(
    raiden: "RaidenService",
    chain_state: ChainState,
    new_balance_proof: BalanceProofSignedState,
    non_closing_participant: Address,
) -> None:
    if raiden.config.services.monitoring_enabled is False:
        return

    msg = "Monitoring is enabled but the default monitoring service address is None."
    assert raiden.default_msc_address is not None, msg

    channel_state = views.get_channelstate_by_canonical_identifier(
        chain_state=chain_state, canonical_identifier=new_balance_proof.canonical_identifier
    )

    msg = (
        f"Failed to update monitoring service due to inability to find "
        f"channel: {new_balance_proof.channel_identifier} "
        f"token_network_address: {to_checksum_address(new_balance_proof.token_network_address)}."
    )
    assert channel_state, msg

    msg = "Monitoring is enabled but the `UserDeposit` contract is None."
    assert raiden.default_user_deposit is not None, msg
    rei_balance = raiden.default_user_deposit.effective_balance(raiden.address, BLOCK_ID_LATEST)
    if rei_balance < MONITORING_REWARD:
        rdn_balance = to_rdn(rei_balance)
        rdn_reward = to_rdn(MONITORING_REWARD)
        log.warning(
            f"Skipping update to Monitoring service. "
            f"Your deposit balance {rdn_balance} is less than "
            f"the required monitoring service reward of {rdn_reward}"
        )
        return

    # In production there should be no MonitoringRequest if
    # channel balance is below a certain threshold. This is
    # a naive approach that needs to be worked on in the future
    if raiden.config.environment_type == Environment.PRODUCTION:
        message = (
            "Skipping update to Monitoring service. "
            "Your channel balance {channel_balance} is less than "
            "the required minimum balance of {min_balance} "
        )

        dai_token_network_address = views.get_token_network_address_by_token_address(
            chain_state=chain_state,
            token_network_registry_address=raiden.default_registry.address,
            token_address=DAI_TOKEN_ADDRESS,
        )
        weth_token_network_address = views.get_token_network_address_by_token_address(
            chain_state=chain_state,
            token_network_registry_address=raiden.default_registry.address,
            token_address=WETH_TOKEN_ADDRESS,
        )
        channel_balance = get_balance(
            sender=channel_state.our_state,
            receiver=channel_state.partner_state,
        )

        if channel_state.canonical_identifier.token_network_address == dai_token_network_address:
            if channel_balance < MIN_MONITORING_AMOUNT_DAI:
                data = dict(
                    channel_balance=channel_balance,
                    min_balance=MIN_MONITORING_AMOUNT_DAI,
                    channel_id=channel_state.canonical_identifier.channel_identifier,
                    token_address=to_checksum_address(DAI_TOKEN_ADDRESS),
                )
                log.warning(message.format(**data), **data)
                return
        if channel_state.canonical_identifier.token_network_address == weth_token_network_address:
            if channel_balance < MIN_MONITORING_AMOUNT_WETH:
                data = dict(
                    channel_balance=channel_balance,
                    min_balance=MIN_MONITORING_AMOUNT_WETH,
                    channel_id=channel_state.canonical_identifier.channel_identifier,
                    token_address=to_checksum_address(WETH_TOKEN_ADDRESS),
                )
                log.warning(message.format(**data), **data)
                return

    log.info(
        "Received new balance proof, creating message for Monitoring Service.",
        node=to_checksum_address(raiden.address),
        balance_proof=new_balance_proof,
    )

    monitoring_message = RequestMonitoring.from_balance_proof_signed_state(
        balance_proof=new_balance_proof,
        non_closing_participant=non_closing_participant,
        reward_amount=MONITORING_REWARD,
        monitoring_service_contract_address=raiden.default_msc_address,
    )
    monitoring_message.sign(raiden.signer)
    raiden.transport.broadcast(monitoring_message, device_id=DeviceIDs.MS)
