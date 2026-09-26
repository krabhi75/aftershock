# Aftershock standing rule

When you change code under `harborline/`:

- A function that assigns `.status` must return early when `event_id` is already in `applied_events`, then record the id. `confirm_delivery` is the pattern.
- A function that asks for the current time must call `datetime.now(timezone.utc)` or take an aware datetime from its caller. A bare `datetime.now()` or `datetime.utcnow()` is the INC-1108 fault.
- Two or more `write_*` or `emit_*` calls must sit inside `with store.unit_of_work()`, or inside a `try` whose handler calls `void_*`, `rollback*`, or `compensate*`. `print_outbound_label` is the pattern.

If a change breaks one of these, name the incident class and fix the shape before finishing the task.
