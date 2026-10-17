---
title: Realtime events
---

Lex App pushes two kinds of events to open browser tabs over WebSockets: `record_mutation` when a record is created, changed or deleted (an open grid refreshes), and calculation-status events while a calculation runs. By default every signed-in socket receives every event — fine for one team, but in a multi-tenant installation it tells everyone which models change and which records are calculating, including error messages.

## Scope delivery per tenant

```python title="lex_config.py"
MUTATION_GROUPS = "myproject.realtime.record_groups"   # (record or model class) -> list[str]
USER_GROUPS = "myproject.realtime.user_groups"         # (user) -> list[str]
```

```python title="myproject/realtime.py"
def record_groups(target):
    tenant = getattr(target, "tenant_id", None)
    return [f"tenant-{tenant}"] if tenant else []

def user_groups(user):
    return [f"tenant-{m.tenant_id}" for m in user.memberships.all()]
```

With both set, an event reaches only sockets whose user shares a group with the record; anonymous sockets receive nothing, and the list of running calculations a socket gets on connect is filtered the same way. A bulk change passes the model class instead of a record. An update reaches the groups of the record before and after the change, each group once, so a record moved to another tenant leaves the old tenant's grid and appears in the new one's. Payloads do not change, so the bundled frontend works as before.

## Silence a model

```python
class AuditTrail(LexModel):
    broadcast_mutations = False
```

No `record_mutation` events for this model at all.
