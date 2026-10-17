---
title: "Grid Filter API"
---

The grid's [[using-the-app/the-grid/filtering and sorting#Value Lists|value lists]] and
[[using-the-app/the-grid/filtering and sorting#The Filter Bar|filter bar]] run on two
endpoints, and the list endpoint's GET has a lookup for the blanks they list. This page
is for calling them yourself — from a script, or from a dashboard of your own. Which
columns get a value list is explained under
[[model-your-data/serializers#Value lists and the filter bar|Serializers]].

They take the same sign-in as the rest of Lex App's API, and apply the user's read
permissions exactly as the grid does;
[[access-and-dashboards/reflex/sessions and authentication#Calling the Lex App API as the user|Calling the Lex App API as the user]]
shows a request with a bearer token. Paths are relative to Lex App's own address.

## Which columns have a value list

`GET api/model_info/<model>/fields` describes a list's columns, for the serializer
`?serializer=` names (`default` when it is left out). Every field carries `value_list`:

```json
{
  "fields": [
    {"name": "status", "type": "string", "choices": [...], "value_list": true, ...},
    {"name": "region", "type": "foreign_key", "target": "region", "value_list": true, ...},
    {"name": "notes", "type": "string", "value_list": false, ...}
  ],
  "id_field": "id",
  "list_ui": {"hide_actions_column": false, "filter_bar": ["status", "region"]}
}
```

- `value_list` is `true` exactly when `filter_values` lists that column's values through
  this serializer, and `Meta.filter_bar` accepts the same columns. A field with no
  database column behind it is always `false`.
- The grid offers a value list on every column where it is `true`, except the primary
  key.
- `list_ui.filter_bar` is the list's default filter bar — `Meta.filter_bar`, or the
  model's `filter_bar` — with every name that isn't a value-list column already dropped.

## A column's values: `filter_values`

`POST api/model_entries/<model>/filter_values`

`as_of` and `serializer` are query parameters, read exactly as the list endpoint reads
them. The body:

```json
{
  "field": "region",
  "filterModel": {
    "status": {"filterType": "set", "values": ["open", "overdue"]}
  },
  "selected": ["3"],
  "limit": 200
}
```

| Key | Required | Meaning |
|---|---|---|
| `field` | yes | The column to list, by name: a value-list column of this list |
| `filterModel` | no | The grid's filter model, in AG Grid's format. Every entry applies except `field`'s own, so the answer is what the *other* filters leave |
| `selected` | no | The keys ticked now. Each appears in the answer even when no row has it any more. The first 1,000 are read |
| `search` | no | Keeps the values whose label contains this text, ignoring case — `"no"` keeps *North* |
| `limit` | no | How many values to return. Default `200`, at most `1000` |

The answer:

```json
{
  "values": [
    {"key": "3", "label": "North", "count": 41},
    {"key": "5", "label": "South", "count": 12},
    {"key": null, "label": "(Blank)", "count": 3}
  ],
  "truncated": false
}
```

| Key | Meaning |
|---|---|
| `key` | The stored value as a string: a related record's primary key, `"true"` or `"false"`, a date as `YYYY-MM-DD`, a number. `null` is blank — on a text column without choices, empty text too. It is the key a `set` filter takes |
| `label` | What the value list shows: the choice's label, the related record's name (its `__str__`), `Yes` or `No`, `(Blank)`, or else the key itself |
| `count` | The rows with this value, under the other filters |
| `truncated` | `true` when the list is not complete: more values matched than `limit`, or the server stopped counting — after 5,000 distinct values, or after reading 50,000 rows of a model whose read permission is decided row by row. Narrow it with `search` |

- Values are sorted by label — integer columns numerically — with blank last.
- A key from `selected` that missed the cut is added after it, with its count or `0`, so
  `values` can be longer than `limit`. While `search` is set, only the ones whose label
  matches are added.
- A row the user may not read is never counted. On a model whose read permission can
  hide a field on some rows, only the rows where the user may read this column count.
  A ticked key that no readable row holds is listed under its own key, never under the
  related record's name.

### Set and multi filters

`filterModel` takes AG Grid's condition filters, and the two shapes value lists add.
The list endpoint and exports read them the same way:

| Shape | Matches |
|---|---|
| `{"filterType": "set", "values": ["open", null]}` | Rows whose column holds any of the keys, written as `key` above. `null` matches blank. An empty `values` list matches no rows |
| `{"filterType": "multi", "filterModels": [condition, set]}` | Rows that match both parts. Either part may be `null` |

The grid never sends an empty `set`: a value list with nothing ticked leaves the column
out of the filter model.

### Errors

| Status | Body | When |
|---|---|---|
| `400` | `{"field": "'notes' is not filterable."}` | `field` isn't a value-list column of this list. The message is the same whatever the reason |
| `400` | `{"filterModel": {"year": "'abc' is not a valid value for year."}}` | A `set` key that can't be read as the column's type — the list endpoint answers the same |
| `400` | `{"filterModel": "must be an object"}` or `{"selected": "must be a list"}` | The body has the wrong shape |
| `405` | | The request is a `GET` |

## The (Blank) lookup on the list GET

`GET api/model_entries/<model>/list` narrows its rows by query parameters, such as
`?status=open` or `?year__gte=2025`. The `__blank` lookup finds the rows a value list's
*(Blank)* finds:

| Parameter | Keeps |
|---|---|
| `?region__blank=true` | The rows whose `region` is blank |
| `?region__blank=false` | Every other row |

- Blank means NULL — and on a text column without choices, empty text as well.
- Only a column of the model itself, a foreign key included: `customer__blank` tests the
  foreign key. A path through a relation (`customer__name__blank`) or into a JSON field
  is ignored, like any lookup the list doesn't know.
- A value other than `true` or `false`, in any letter case, is ignored too.

## See also

- [[using-the-app/the-grid/filtering and sorting|Filtering & Sorting]] — value lists and the filter bar, as users see them
- [[model-your-data/serializers#Value lists and the filter bar|Serializers]] — which columns get a value list, and `Meta.filter_bar`
- [[access-and-dashboards/streamlit/embedding app pages#Filtering the embedded table|Embedding App Pages]] — an embedded table's filters, set from Python
