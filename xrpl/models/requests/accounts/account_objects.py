"""
This request returns the raw ledger format for all objects owned by an account.

For a higher-level view of an account's trust lines and balances, see
AccountLinesRequest instead.

`See account_objects <https://xrpl.org/account_objects.html>`_
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional, Union

from xrpl.models.base_model import REQUIRED
from xrpl.models.requests.request import Request, RequestMethod


class AccountObjectType(str, Enum):
    """Represents the object types that an AccountObjectsRequest can ask for."""

    CHECK = "check"
    DEPOSIT_PREAUTH = "deposit_preauth"
    ESCROW = "escrow"
    OFFER = "offer"
    PAYMENT_CHANNEL = "payment_channel"
    SIGNER_LIST = "signer_list"
    STATE = "state"
    TICKET = "ticket"


@dataclass(frozen=True)
class AccountObjects(Request):
    """
    This request returns the raw ledger format for all objects owned by an account.

    For a higher-level view of an account's trust lines and balances, see
    AccountLinesRequest instead.

    `See account_objects <https://xrpl.org/account_objects.html>`_
    """

    account: str = REQUIRED
    ledger_hash: Optional[str] = None
    ledger_index: Optional[Union[str, int]] = None
    method: RequestMethod = field(default=RequestMethod.ACCOUNT_OBJECTS, init=False)
    type: Optional[AccountObjectType] = None
    deletion_blockers_only: Optional[bool] = False
    limit: Optional[int] = None
    marker: Optional[Any] = None