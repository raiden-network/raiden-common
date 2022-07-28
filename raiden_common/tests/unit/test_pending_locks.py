from raiden_common.constants import LOCKSROOT_OF_NO_LOCKS
from raiden_common.transfer.channel import compute_locksroot
from raiden_common.transfer.state import PendingLocksState


def test_empty():
    locks = PendingLocksState([])
    assert compute_locksroot(locks) == LOCKSROOT_OF_NO_LOCKS
