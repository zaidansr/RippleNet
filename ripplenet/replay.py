"""Ordinal replay and delayed outcomes for synthetic causal-boundary checks.

This is not a market-data adapter or evidence that an archive preserves original
availability. The caller must supply an already admissible, append-only order.
Every supplied price or notice occupies one ordinal; there is no receiver clock.
Notices label qualifying corrections but do not rewrite as-recorded prices.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Context, Decimal, localcontext
from typing import Literal


def _integer(value: int, name: str, minimum: int = 0) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")


def _identifier(value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Identifiers must be nonempty strings")


def _log_return(start: Decimal, end: Decimal) -> float:
    # Fix precision independently of a caller's ambient Decimal context.
    with localcontext(Context(prec=34)):
        return float(end.ln() - start.ln())


@dataclass(frozen=True)
class PriceRecord:
    """A positive recorded price at an ordinal, not a latent or revised price."""

    ordinal: int
    record_id: str
    price: Decimal

    def __post_init__(self) -> None:
        _integer(self.ordinal, "ordinal")
        _identifier(self.record_id)
        if not isinstance(self.price, Decimal) or not self.price.is_finite() or self.price <= 0:
            raise ValueError("price must be a finite positive Decimal")


@dataclass(frozen=True)
class CorrectionNotice:
    """A qualifying notice linked to a previously consumed price record.

    Its economic meaning must be defined by the caller's task. A notice is not
    automatically a pure recording-error label or a replacement-price message.
    """

    ordinal: int
    notice_id: str
    record_id: str

    def __post_init__(self) -> None:
        _integer(self.ordinal, "ordinal")
        _identifier(self.notice_id)
        _identifier(self.record_id)


Message = PriceRecord | CorrectionNotice


@dataclass(frozen=True)
class Snapshot:
    """Immutable prefix features; absent price/history is represented by None."""

    ordinal: int = -1
    price_id: str | None = None
    price: Decimal | None = None
    price_updates: int = 0
    correction_notices: int = 0
    last_recorded_return: float | None = None


@dataclass(frozen=True)
class Outcome:
    """An outcome and its availability ordinal, separate from input features.

    An observed zero correction label means no qualifying notice within the
    window, never a verified genuine shock. Non-observed outcomes have no value.
    """

    status: Literal["observed", "pending", "censored", "unavailable"]
    value: float | int | None = None
    available_at: int | None = None

    def __post_init__(self) -> None:
        if self.status not in ("observed", "pending", "censored", "unavailable"):
            raise ValueError("Unknown outcome status")
        if self.status == "observed":
            if isinstance(self.value, bool) or not isinstance(self.value, (int, float)):
                raise ValueError("Observed outcomes need a numeric value")
            from math import isfinite

            if not isfinite(self.value):
                raise ValueError("Observed outcomes must be finite")
            _integer(self.available_at, "available_at")  # type: ignore[arg-type]
        elif self.value is not None or self.available_at is not None:
            raise ValueError("Unobserved outcomes cannot carry a value or availability")


class Replay:
    """Consume a validated ordinal prefix without sorting or revising history.

    Use a separate replay stopped at each historical fit cursor. Sealing means
    the supplied interval ended; it does not certify complete market coverage.
    This small research implementation retains snapshots in memory.
    """

    def __init__(self) -> None:
        self._snapshots: list[Snapshot] = []
        self._price_origins: dict[str, int] = {}
        self._first_notices: dict[str, int] = {}
        self._message_ids: set[str] = set()
        self._closed = False

    @property
    def snapshot(self) -> Snapshot:
        """Return the current immutable prefix; no outcome labels are included."""
        return self._snapshots[-1] if self._snapshots else Snapshot()

    def consume(self, message: Message) -> Snapshot:
        """Append one message atomically; reject gaps, duplicate IDs and bad links."""
        if self._closed:
            raise ValueError("Replay is sealed")
        if not isinstance(message, (PriceRecord, CorrectionNotice)):
            raise TypeError("Expected a PriceRecord or CorrectionNotice")
        if message.ordinal != len(self._snapshots):
            raise ValueError("Ordinals must be contiguous, starting at zero")
        message_id = message.record_id if isinstance(message, PriceRecord) else message.notice_id
        if message_id in self._message_ids:
            raise ValueError("Duplicate message identifier")
        previous = self.snapshot
        if isinstance(message, PriceRecord):
            change = None if previous.price is None else _log_return(previous.price, message.price)
            current = Snapshot(
                message.ordinal, message.record_id, message.price,
                previous.price_updates + 1, previous.correction_notices, change,
            )
            self._price_origins[message.record_id] = message.ordinal
        else:
            if message.record_id not in self._price_origins:
                raise ValueError("Correction must link to an earlier price record")
            current = Snapshot(
                message.ordinal, previous.price_id, previous.price,
                previous.price_updates, previous.correction_notices + 1,
                previous.last_recorded_return,
            )
            self._first_notices.setdefault(message.record_id, message.ordinal)
        self._message_ids.add(message_id)
        self._snapshots.append(current)
        return current

    def seal(self) -> None:
        """Mark the interval complete; unfinished windows become censored."""
        self._closed = True

    def _origin(self, ordinal: int) -> Snapshot:
        _integer(ordinal, "origin ordinal")
        if ordinal >= len(self._snapshots):
            raise ValueError("Origin is not in the consumed prefix")
        return self._snapshots[ordinal]

    def _unfinished(self) -> Outcome:
        return Outcome("censored" if self._closed else "pending")

    def recorded_return(self, origin_ordinal: int, horizon: int) -> Outcome:
        """Return log(P[k+H])-log(P[k]) after exactly H supplied messages.

        P is the last as-recorded price, including carry-forward at a notice.
        A constant price is a valid zero target. This is not a trading return.
        """
        _integer(horizon, "horizon", 1)
        origin = self._origin(origin_ordinal)
        if origin.price is None:
            return Outcome("unavailable")
        endpoint = origin_ordinal + horizon
        if endpoint >= len(self._snapshots):
            return self._unfinished()
        future = self._snapshots[endpoint]
        assert future.price is not None
        return Outcome("observed", _log_return(origin.price, future.price), endpoint)

    def correction_label(self, record_id: str, window: int) -> Outcome:
        """A notice in (origin, origin+L], released only at full-window maturity.

        Both positives and negatives wait until origin+L. Even an early positive
        is censored if this interval ends before the declared maturity boundary.
        This conservative policy avoids different ascertainment times by class.
        """
        _identifier(record_id)
        _integer(window, "window", 1)
        if record_id not in self._price_origins:
            raise ValueError("Unknown price record")
        deadline = self._price_origins[record_id] + window
        if deadline >= len(self._snapshots):
            return self._unfinished()
        first_notice = self._first_notices.get(record_id)
        value = int(first_notice is not None and first_notice <= deadline)
        return Outcome("observed", value, deadline)


def training_eligible(target: Outcome, label: Outcome, fit_ordinal: int) -> bool:
    """Require both observed outcomes to have matured by the historical fit.

    Necessary timing check only: this does not perform a split, fit a model,
    certify feature provenance or protect against user-supplied fabricated data.
    """
    _integer(fit_ordinal, "fit ordinal")
    return (
        target.status == label.status == "observed"
        and target.available_at is not None
        and label.available_at is not None
        and max(target.available_at, label.available_at) <= fit_ordinal
    )
