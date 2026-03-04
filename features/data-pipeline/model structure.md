---
title: Model Structure
---

By default, all your models appear as a flat list in the frontend sidebar. If you have many models, you can organize them into groups and subgroups using a `model_structure.yaml` file.

## Configuration

Create a `model_structure.yaml` file in your project root:

```yaml title="model_structure.yaml"
- group: Fund Management
  models:
    - Fund
    - Quarter
    - subgroup: Investments
      models:
        - Investment
        - InvestmentRelationship

- group: Reporting
  models:
    - CalculateNAV
    - CalculateBalanceSheet

- group: Uploads
  models:
    - UploadBalanceSheet
    - UploadInvestmentRelationships
```

This creates a nested sidebar structure in the frontend with collapsible groups.

> [!tip]
> `model_structure.yaml` is optional. Without it, all models appear alphabetically in a flat list. Add it when your project grows beyond a handful of models.

## Model Styling

You can customize how individual models appear in the frontend by defining a `model_styling` class method:

```python title="Team.py"
class Team(LexModel):
    name = models.CharField(max_length=200)

    @classmethod
    def model_styling(cls):
        return {
            "icon": "👥",
            "color": "#4CAF50",
            "display_name": "Teams"
        }
```

## Hiding Models

If you have models that shouldn't appear in the frontend at all (e.g., internal lookup tables), use `untracked_models`:

```python title="_authentication_settings.py"
untracked_models = ['InternalLookup', 'SystemConfig']
```

Models listed here won't appear in the sidebar or be accessible through the frontend UI, but they remain fully functional in your backend code.
