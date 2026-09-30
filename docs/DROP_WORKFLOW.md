# Drop Workflow

Buildwright uses numbered ZIP drops as the handoff unit.

## Naming

```text
Buildwright_DROP_0001_REPO_FOUNDATION.zip
Buildwright_DROP_0002_<PURPOSE>.zip
Buildwright_DROP_0003_<PURPOSE>.zip
```

## Standard drop contents

```text
README_FIRST.md
APPLY_DROP.ps1
ROLLBACK_LAST_DROP.ps1
drop.json
SHA256SUMS.txt
payload/
```

## Apply behavior

The applier:

1. verifies package checksums;
2. backs up files that will be overwritten;
3. overlays `payload/` into the selected repo;
4. runs the repository validator;
5. initializes Git when necessary;
6. stages and commits the drop;
7. pushes to `origin` when one is configured and push is not disabled.

Backups are stored under `.buildwright_drop_backups/` and are gitignored.

## Repository authority

After a drop is applied and committed, Git becomes authoritative. The ZIP remains a reproducible handoff artifact.
