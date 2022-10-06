from pathlib import Path
from typing import *  # NOQA pylint:disable=wildcard-import,unused-wildcard-import
from typing import TYPE_CHECKING, Any, Dict, Literal, NewType, Tuple, Type, Union

from eth_typing import (  # NOQA pylint:disable=unused-import
    Address,
    BlockNumber,
    ChecksumAddress,
    Hash32,
    HexAddress,
)
from web3.types import ABI, BlockIdentifier, Nonce  # NOQA pylint:disable=unused-import

from raiden_contracts.contract_manager import CompiledContract  # NOQA pylint:disable=unused-import
from raiden_contracts.utils.type_aliases import (  # NOQA pylint:disable=unused-import
    AdditionalHash,
    BalanceHash,
    BlockExpiration,
    ChainID,
    ChannelID,
    Locksroot,
    PrivateKey,
    Signature,
    T_AdditionalHash,
    T_BalanceHash,
    T_BlockExpiration,
    T_ChainID,
    T_ChannelID,
    T_Locksroot,
    T_PrivateKey,
    T_Signature,
    T_TokenAmount,
    TokenAmount,
)

if TYPE_CHECKING:
    # pylint: disable=unused-import
    from raiden_common.exceptions import (  # noqa: F401
        RaidenRecoverableError,
        RaidenUnrecoverableError,
    )
    from raiden_common.messages.monitoring_service import SignedBlindedBalanceProof  # noqa: F401
    from raiden_common.transfer.mediated_transfer.state import (  # noqa: F401
        InitiatorTransferState,
        LockedTransferSignedState,
        LockedTransferUnsignedState,
    )
    from raiden_common.transfer.state import (  # noqa: F401
        HashTimeLockState,
        NettingChannelState,
        NetworkState,
        UnlockPartialProofState,
    )


MYPY_ANNOTATION = "This assert is used to tell mypy what is the type of the variable"


def typecheck(value: Any, expected: Union[Type, Tuple[Type, ...]]) -> None:
    if not isinstance(value, expected):
        raise ValueError(f"Expected a value of type {expected}, got value of type {type(value)}")


T_EVMBytecode = bytes
EVMBytecode = NewType("EVMBytecode", T_EVMBytecode)

GasMeasurements = Dict[str, int]


T_Address = bytes

AddressHex = HexAddress

T_Balance = int
Balance = NewType("Balance", int)

T_GasPrice = int
GasPrice = NewType("GasPrice", int)

T_BlockGasLimit = int
BlockGasLimit = NewType("BlockGasLimit", int)

T_BlockHash = bytes
BlockHash = Hash32

T_BlockNumber = int

T_Timestamp = int
Timestamp = NewType("Timestamp", int)

# A relative number of blocks
T_BlockTimeout = int
BlockTimeout = NewType("BlockTimeout", int)

T_ChannelState = int
ChannelState = NewType("ChannelState", int)

T_InitiatorAddress = bytes
InitiatorAddress = NewType("InitiatorAddress", bytes)

T_MessageID = int
MessageID = NewType("MessageID", int)

T_Nonce = int

T_NetworkTimeout = float
NetworkTimeout = NewType("NetworkTimeout", float)

T_PaymentID = int
PaymentID = NewType("PaymentID", int)

# PaymentAmount is for amounts of tokens paid end-to-end
T_PaymentAmount = int
PaymentAmount = NewType("PaymentAmount", int)

T_PublicKey = bytes
PublicKey = NewType("PublicKey", bytes)

T_FeeAmount = int
FeeAmount = NewType("FeeAmount", int)

# A proportional fee, unit is parts-per-million
# 1_000_000 means 100%, 25_000 is 2.5%
T_ProportionalFeeAmount = int
ProportionalFeeAmount = NewType("ProportionalFeeAmount", int)

T_LockedAmount = int
LockedAmount = NewType("LockedAmount", int)

T_PaymentWithFeeAmount = int
PaymentWithFeeAmount = NewType("PaymentWithFeeAmount", int)

T_TokenNetworkRegistryAddress = bytes
TokenNetworkRegistryAddress = NewType("TokenNetworkRegistryAddress", bytes)

T_RaidenProtocolVersion = int
RaidenProtocolVersion = NewType("RaidenProtocolVersion", int)

T_RaidenDBVersion = int
RaidenDBVersion = NewType("RaidenDBVersion", int)

T_TargetAddress = bytes
TargetAddress = NewType("TargetAddress", bytes)

T_TokenAddress = bytes
TokenAddress = NewType("TokenAddress", bytes)

T_UserDepositAddress = bytes
UserDepositAddress = NewType("UserDepositAddress", bytes)

T_MonitoringServiceAddress = bytes
MonitoringServiceAddress = NewType("MonitoringServiceAddress", bytes)

T_ServiceRegistryAddress = bytes
ServiceRegistryAddress = NewType("ServiceRegistryAddress", bytes)

T_OneToNAddress = bytes
OneToNAddress = NewType("OneToNAddress", bytes)

T_TokenNetworkAddress = bytes
TokenNetworkAddress = NewType("TokenNetworkAddress", bytes)

T_TransferID = bytes
TransferID = NewType("TransferID", bytes)

T_Secret = bytes
Secret = NewType("Secret", bytes)

T_EncryptedSecret = bytes
EncryptedSecret = NewType("EncryptedSecret", bytes)

T_SecretHash = bytes
SecretHash = NewType("SecretHash", bytes)

T_SecretRegistryAddress = bytes
SecretRegistryAddress = NewType("SecretRegistryAddress", bytes)

T_TransactionHash = bytes
TransactionHash = NewType("TransactionHash", bytes)

T_EncodedData = bytes
EncodedData = NewType("EncodedData", bytes)

T_WithdrawAmount = int
WithdrawAmount = NewType("WithdrawAmount", int)

T_MetadataHash = bytes
MetadataHash = NewType("MetadataHash", bytes)

NodeNetworkStateMap = Dict[Address, "NetworkState"]

Host = NewType("Host", str)
Port = NewType("Port", int)
HostPort = Tuple[Host, Port]
Endpoint = NewType("Endpoint", str)

LockType = Union["HashTimeLockState", "UnlockPartialProofState"]
ErrorType = Union[Type["RaidenRecoverableError"], Type["RaidenUnrecoverableError"]]
LockedTransferType = Union["LockedTransferUnsignedState", "LockedTransferSignedState"]

DatabasePath = Union[Path, Literal[":memory:"]]

T_PeerCapabilities = Dict[str, Union[str, bool]]
PeerCapabilities = NewType("PeerCapabilities", Dict)

T_UserID = str
UserID = NewType("UserID", str)

AddressMetadata = Dict[str, Union[UserID, str]]

AddressTypes = Union[
    Address,
    TokenAddress,
    TokenNetworkAddress,
    TokenNetworkRegistryAddress,
    MonitoringServiceAddress,
    TargetAddress,
    InitiatorAddress,
    OneToNAddress,
    SecretRegistryAddress,
    ServiceRegistryAddress,
    UserDepositAddress,
]
