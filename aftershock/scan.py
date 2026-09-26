"""Structural sibling scan.

The scan is deterministic on purpose. It spends zero Bobcoins and gives Bob a
short list of sites, so Agent mode spends the 40-coin budget on confirming,
testing, and patching rather than on re-reading the tree.
"""

from __future__ import annotations

import ast
from pathlib import Path

from aftershock.models import Finding, FunctionSite

_GUARD_CALLS = {"already_applied", "ensure_once"}
_COMPENSATE_PREFIXES = ("void_", "rollback", "compensate")
_WRITE_PREFIXES = ("write_", "emit_")


def _dotted(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _dotted(node.value)
        if base is None:
            return None
        return f"{base}.{node.attr}"
    return None


def _call_tail(node: ast.Call) -> str:
    dotted = _dotted(node.func) or ""
    return dotted.split(".")[-1]


def _assigns_status(func: ast.AST) -> bool:
    for node in ast.walk(func):
        targets: list[ast.expr] = []
        if isinstance(node, ast.Assign):
            targets = list(node.targets)
        elif isinstance(node, ast.AnnAssign):
            targets = [node.target]
        elif isinstance(node, ast.AugAssign):
            targets = [node.target]
        for target in targets:
            if isinstance(target, ast.Attribute) and target.attr == "status":
                return True
    return False


def _has_idempotency_guard(func: ast.AST) -> bool:
    for node in ast.walk(func):
        if isinstance(node, ast.Compare):
            for op, comparator in zip(node.ops, node.comparators):
                if not isinstance(op, (ast.In, ast.NotIn)):
                    continue
                dotted = _dotted(comparator) or ""
                if dotted == "applied_events" or dotted.endswith(".applied_events"):
                    return True
        if isinstance(node, ast.Call) and _call_tail(node) in _GUARD_CALLS:
            return True
    return False


def _naive_now_calls(func: ast.AST) -> list[str]:
    found: list[str] = []
    for node in ast.walk(func):
        if not isinstance(node, ast.Call):
            continue
        dotted = _dotted(node.func) or ""
        if dotted == "datetime.utcnow":
            found.append(dotted)
            continue
        if dotted == "datetime.now" and not node.args and not node.keywords:
            found.append(dotted)
    return found


def _is_effect_write(node: ast.Call) -> bool:
    return _call_tail(node).startswith(_WRITE_PREFIXES)


def _with_is_unit_of_work(node: ast.With) -> bool:
    for item in node.items:
        expr = item.context_expr
        if isinstance(expr, ast.Call) and _call_tail(expr) == "unit_of_work":
            return True
    return False


def _handler_compensates(node: ast.Try) -> bool:
    for handler in node.handlers:
        for inner in ast.walk(handler):
            if isinstance(inner, ast.Call) and _call_tail(inner).startswith(_COMPENSATE_PREFIXES):
                return True
    return False


def _unprotected_writes(func: ast.AST) -> list[ast.Call]:
    protected: set[int] = set()
    for node in ast.walk(func):
        regions: list[ast.AST] = []
        if isinstance(node, ast.With) and _with_is_unit_of_work(node):
            regions.append(node)
        if isinstance(node, ast.Try) and _handler_compensates(node):
            regions.append(node)
        for region in regions:
            for inner in ast.walk(region):
                if isinstance(inner, ast.Call) and _is_effect_write(inner):
                    protected.add(id(inner))
    writes: list[ast.Call] = []
    for node in ast.walk(func):
        if isinstance(node, ast.Call) and _is_effect_write(node) and id(node) not in protected:
            writes.append(node)
    writes.sort(key=lambda call: call.lineno)
    return writes


def match_function(func: ast.FunctionDef | ast.AsyncFunctionDef, fault_class: str) -> tuple[str, str] | None:
    """Return (reason, recommended change) when func has this fault shape."""
    if fault_class == "retry_blind_write":
        if _assigns_status(func) and not _has_idempotency_guard(func):
            return (
                "Assigns .status and never checks applied_events or already_applied.",
                "Return early when event_id is already in parcel.applied_events, record the id, then assign status. Match confirm_delivery.",
            )
        return None
    if fault_class == "naive_deadline":
        calls = _naive_now_calls(func)
        if calls:
            names = ", ".join(calls)
            return (
                f"Calls {names} with no timezone.",
                "Call datetime.now(timezone.utc) instead of datetime.now() with no argument. Match hub_intake_deadline.",
            )
        return None
    if fault_class == "partial_commit":
        writes = _unprotected_writes(func)
        if len(writes) >= 2:
            names = ", ".join(_call_tail(call) for call in writes)
            return (
                f"Calls {names} with no unit_of_work and no compensating except.",
                "Wrap the writes in with store.unit_of_work(), as print_outbound_label does, so a failed later write rolls the earlier one back.",
            )
        return None
    raise ValueError(f"unknown fault class {fault_class}")


def scan_source(source: str, module: str, fault_class: str, file: str = "") -> tuple[list[Finding], list[FunctionSite]]:
    tree = ast.parse(source)
    findings: list[Finding] = []
    sites: list[FunctionSite] = []
    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if node.name.startswith("_"):
            continue
        symbol = f"{module}.{node.name}"
        sites.append(FunctionSite(symbol=symbol, file=file, line=node.lineno))
        matched = match_function(node, fault_class)
        if matched is None:
            continue
        reason, change = matched
        findings.append(
            Finding(
                symbol=symbol,
                file=file,
                line=node.lineno,
                fault_class=fault_class,
                reason=reason,
                recommended_change=change,
            )
        )
    return findings, sites


def iter_product_files(root: Path) -> list[tuple[Path, str]]:
    package = root / "harborline"
    files: list[tuple[Path, str]] = []
    for path in sorted(package.glob("*.py")):
        files.append((path, f"harborline.{path.stem}"))
    return files


def scan_tree(root: Path, fault_class: str) -> tuple[list[Finding], dict[str, FunctionSite]]:
    findings: list[Finding] = []
    index: dict[str, FunctionSite] = {}
    for path, module in iter_product_files(root):
        source = path.read_text(encoding="utf-8")
        relative = path.relative_to(root).as_posix()
        found, sites = scan_source(source, module, fault_class, file=relative)
        findings.extend(found)
        for site in sites:
            index[site.symbol] = site
    findings.sort(key=lambda item: (item.file, item.line, item.symbol))
    return findings, index
