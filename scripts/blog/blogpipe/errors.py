"""The one exception every gate raises (callers map it to exit 65) and the run identity type."""

from __future__ import annotations


class ContractError(ValueError):
    pass


class PublicationError(ValueError):
    """An unverifiable handoff or failed delivery transaction remains pending."""


# date / slug / run_id: the exact scope every staged record, receipt and append must carry.
Identity = dict[str, str]
