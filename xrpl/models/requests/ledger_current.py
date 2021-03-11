"""
The ledger_current method returns the unique
identifiers of the current in-progress ledger.
This command is mostly useful for testing,
because the ledger returned is still in flux.
"""
from dataclasses import dataclass, field

from xrpl.models.requests.request import Request, RequestMethod


@dataclass(frozen=True)
class LedgerCurrent(Request):
    """
    The ledger_current method returns the unique
    identifiers of the current in-progress ledger.
    This command is mostly useful for testing,
    because the ledger returned is still in flux.
    """

    method: RequestMethod = field(default=RequestMethod.LEDGER_CURRENT, init=False)