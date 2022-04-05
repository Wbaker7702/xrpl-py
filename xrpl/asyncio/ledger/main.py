"""High-level ledger methods with the XRPL ledger."""

from typing import Optional, cast

from typing_extensions import Literal

from xrpl.asyncio.clients import Client, XRPLRequestFailureException
from xrpl.constants import XRPLException
from xrpl.models.requests import Fee, Ledger
from xrpl.utils import xrp_to_drops


async def get_latest_validated_ledger_sequence(client: Client) -> int:
    """
    Returns the sequence number of the latest validated ledger.

    Args:
        client: The network client to use to send the request.

    Returns:
        The sequence number of the latest validated ledger.

    Raises:
        XRPLRequestFailureException: if the rippled API call fails.
    """
    response = await client.request_impl(Ledger(ledger_index="validated"))
    if response.is_successful():
        return cast(int, response.result["ledger_index"])

    raise XRPLRequestFailureException(response.result)


async def get_latest_open_ledger_sequence(client: Client) -> int:
    """
    Returns the sequence number of the latest open ledger.

    Args:
        client: The network client to use to send the request.

    Returns:
        The sequence number of the latest open ledger.

    Raises:
        XRPLRequestFailureException: if the rippled API call fails.
    """
    response = await client.request_impl(Ledger(ledger_index="open"))
    if response.is_successful():
        return cast(int, response.result["ledger_index"])

    raise XRPLRequestFailureException(response.result)


async def get_fee(
    client: Client,
    *,
    max_fee: Optional[float] = 2,
    fee_type: Optional[Literal["open", "minimum"]] = None,
) -> str:
    """
    Query the ledger for the current transaction fee.

    Args:
        client: the network client used to make network calls.
        max_fee: The maximum fee in XRP that the user wants to pay. If load gets too
            high, then the fees will not scale past the maximum fee. If None, there is
            no ceiling for the fee. The default is 2 XRP.
        fee_type: The type of fee to return. The options are "open" (the load-scaled
            fee to get into the open ledger) or "minimum" (the minimum transaction
            fee). The default is `None`.

    Returns:
        The transaction fee, in drops.
        Read more about drops: https://xrpl.org/currency-formats.html#xrp-amounts

    Raises:
        XRPLException: if an incorrect option for `fee_type` is passed in.
        XRPLRequestFailureException: if the rippled API call fails.
    """
    response = await client.request_impl(Fee())
    if not response.is_successful():
        raise XRPLRequestFailureException(response.result)

    result = response.result
    if fee_type:
        drops = result["drops"]
        if fee_type == "open":
            fee = cast(str, drops["open_ledger_fee"])
        elif fee_type == "minimum":
            fee = cast(str, drops["minimum_fee"])
        else:
            raise XRPLException(
                f'`fee_type` param must be "open" or "minimum". {fee_type} is not a '
                "valid option."
            )
        if max_fee is not None:
            max_fee_drops = int(xrp_to_drops(max_fee))
            if max_fee_drops < int(fee):
                fee = str(max_fee_drops)
    else:
        current_queue_size = int(result["current_queue_size"])
        max_queue_size = int(result["max_queue_size"])
        queue_pct = current_queue_size / max_queue_size
        drops = result["drops"]
        minimum_fee = int(drops["minimum_fee"])
        median_fee = int(drops["median_fee"])
        open_ledger_fee = int(drops["open_ledger_fee"])

        fee_low = round(
            min(
                max(minimum_fee * 1.5, round(max(median_fee, open_ledger_fee) / 500)),
                1000,
            ),
        )
        if queue_pct > 0.1:
            possible_fee_medium = round(
                (minimum_fee + median_fee + open_ledger_fee) / 3
            )
        elif queue_pct == 0:
            possible_fee_medium = max(
                10 * minimum_fee, min(minimum_fee, open_ledger_fee)
            )
        else:
            possible_fee_medium = max(
                10 * minimum_fee, round((minimum_fee + median_fee) / 2)
            )
        fee_medium = round(
            min(
                possible_fee_medium,
                fee_low * 15,
                10000,
            ),
        )
        fee_high = round(
            min(
                max(10 * minimum_fee, round(max(median_fee, open_ledger_fee) * 1.1)),
                100000,
            ),
        )

        if queue_pct == 1:
            fee = str(fee_high)
        elif queue_pct == 0:
            fee = str(fee_low)
        else:
            fee = str(fee_medium)
    return fee
