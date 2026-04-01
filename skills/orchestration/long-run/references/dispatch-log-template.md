# Dispatch Log Template

Use this format for `Plans/dispatch-log.md`. Append one row per feature dispatch.

```markdown
# Dispatch Log

| Timestamp | ID | Feature | Complexity | Method | Result | Duration |
|-----------|-----|---------|------------|--------|--------|----------|
| 2026-03-27T14:30:00Z | feat-01 | config-parser | S | mini-stack | PASS | 8 min |
| 2026-03-27T14:45:00Z | feat-02 | data-loader | M | mini-stack | PASS | 22 min |
| 2026-03-27T15:10:00Z | feat-03 | core-calculation | L | pi-stack | PASS | 45 min |
```

**Column definitions:**
- **Timestamp**: ISO 8601 UTC when dispatch started
- **ID**: Feature ID from feature-list.json
- **Feature**: Human-readable feature name
- **Complexity**: S / M / L / XL
- **Method**: `mini-stack`, `pi-stack`, or `modular-worker`
- **Result**: `PASS`, `FAIL`, or `BLOCKED`
- **Duration**: Approximate wall-clock time
