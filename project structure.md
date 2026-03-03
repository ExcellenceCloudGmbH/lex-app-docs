---
title: Project Structure
---

LEX uses a flat project structure — no `manage.py`, no nested Django app folders, no `admin.py` or `views.py`. Your model files can live directly at the project root or be organized into subfolders as your project grows.

```
YourProject/
├── .env                        ← environment config (single source of truth)
├── .run/                       ← PyCharm run configurations (auto-generated)
│   ├── Init.run.xml
│   └── Start.run.xml
├── migrations/                 ← Django migrations
├── Tests/
│   ├── basic_test/
│   │   └── test_data.json
│   └── UploadFiles/
├── model_structure.yaml        ← frontend sidebar layout (optional)
├── requirements.txt
├── _authentication_settings.py ← test data + group config
├── Team.py                     ← models at the root
├── Employee.py
├── Expense.py
└── Upload/                     ← or organized into subfolders
    ├── __init__.py
    ├── TeamUpload.py
    └── ExpenseUpload.py
```

## Imports Follow the Folder Structure

Models at the project root are imported with a relative import:

```python
from .Team import Team
```

Models inside a subfolder use the folder name as the package:

```python
from Upload.TeamUpload import TeamUpload
```

You choose how to organize. Small projects can keep everything at the root. Larger projects benefit from grouping related models into folders.

## The `.env` File

The `.env` file is the single source of truth for all runtime configuration. It's loaded automatically by the PyCharm run configurations, or you can source it manually in the terminal with `set -a; source .env; set +a`.

See [[installation]] for how to configure it.

## Model Files

Each model is a standalone Python file. The framework discovers them automatically — you don't need to register them anywhere.

```python title="Team.py"
from lex.core.models.LexModel import LexModel
from django.db import models


class Team(LexModel):
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    budget = models.DecimalField(max_digits=12, decimal_places=2)
```

> [!tip]
> If you need to organize your models in the frontend sidebar, use a `model_structure.yaml` file. See [[features/model structure]] for details.

## Key Dependencies

LEX brings along a specific set of dependencies. Make sure your `requirements.txt` includes:

- `lex-app` — the framework itself
- `pandas`, `numpy` — you manage these versions yourself (not bundled)
- Any additional libraries your project needs

> [!warning]
> If you're upgrading from an older version, `pandas` and `numpy` are no longer bundled with `lex-app`. Add them explicitly to your `requirements.txt` with the versions your project requires.
