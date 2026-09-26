# Fault classes

Aftershock classifies a sibling by structure, not by function name.

## retry_blind_write

Plain name: Retry wrote twice.

A function assigns `.status` and never tests membership in `applied_events` and never calls `already_applied` or `ensure_once`.

Closed pattern: `harborline.movement.confirm_delivery`.

A retried webhook appends the same event twice. The guard returns before the second write.

## naive_deadline

Plain name: Clock forgot its timezone.

A function calls `datetime.now()` with no arguments, or calls `datetime.utcnow()`.

`datetime.now(timezone.utc)` is closed. So is a function that only formats a datetime it received.

Closed pattern: `harborline.clocks.hub_intake_deadline`.

## partial_commit

Plain name: Two writes, no rollback.

A function calls two or more `write_*` or `emit_*` functions that are outside both of these:

- `with store.unit_of_work()`
- a `try` whose `except` calls `void_*`, `rollback*`, or `compensate*`

One write is not this class. A price check that only reads is not this class.

Closed pattern: `harborline.paperwork.print_outbound_label`.
