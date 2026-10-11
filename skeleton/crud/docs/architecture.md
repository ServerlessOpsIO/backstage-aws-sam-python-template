# Architecture

## Physical architecture

```text
Client with Cognito access token
  |
  | HTTPS (Route 53 hostname, ACM certificate)
  v
Regional API Gateway REST API -- Cognito User Pool authorizer
  |                       |
  | CRUD proxy routes     +-- /health mock response
  v
Create / Get / Upsert / Delete Lambda functions
  |
  v
DynamoDB table (pk, sk; on-demand capacity)

Lambda and API Gateway --> CloudWatch logs and metrics
```

`template.yaml` owns the DynamoDB table, four Lambda functions and their
API Gateway invoke permissions, API, certificate, and DNS configuration.
The Cognito pool, hosted zone, SSM hosted-zone parameter, and CI roles are
external dependencies.

Each Lambda has a `DynamoDBCrudPolicy` scoped to this table. API routes are
wired through `openapi.yaml`, not through SAM function `Events`. All functions
receive the table name through `DDB_TABLE_NAME`.

The API stage is named by `CodeBranch`. Its access log group is
`/aws/api-gateway/<stack-name>` with seven-day retention. Detailed logging and
metrics are described in [Observability](observability.md).

## Anatomy of a function

For example, `src/handlers/Create${{ values.collection_name_cap }}Item/` contains
`function.py`, `requirements.txt`, and `__init__.py`.
The SAM resource's `CodeUri` points to that directory and its
`Handler` is `function.handler`.

1. Module initialization creates a Powertools logger, a DynamoDB resource in
   `us-east-1`, and the table reference from the environment.
2. `@LOGGER.inject_lambda_context` enriches logs with invocation context.
3. `@event_source(data_class=APIGatewayProxyEvent)` wraps the incoming API Gateway
   event for access to its body and path parameters.
4. `handler` parses request data into shared dataclasses and delegates database
   work to `_main`.
5. The handler constructs a response-body dataclass and JSON-encodes it into an
   `Output` with `statusCode` and string `body`.
6. `@lambda_dataclass_response` converts the outer dataclass into a dictionary
   suitable for Lambda proxy output. It does not perform schema validation.

Shared model code is in `src/common/common/model/${{ values.collection_name }}.py`.
`Base${{ values.collection_name_cap }}Data` is the place for business fields;
`${{ values.collection_name_cap }}Data` adds the optional API `id`;
`${{ values.collection_name_cap }}ItemKeys` holds `pk` and `sk`; and
`${{ values.collection_name_cap }}Item` combines keys and data for storage.
Its `get_data()` excludes storage keys from the returned data.

Create uses a conditional `put_item` to avoid overwriting an existing key.
Upsert uses a conditional `put_item` requiring an existing key: it replaces
the stored item rather than partially updating attributes.

## Anatomy of a test

`tests/unit/handlers/Create${{ values.collection_name_cap }}Item/test_function.py`
illustrates the starter pattern:

- Constants locate the function's fixtures under `./data/handlers/<function>/`.
- Pytest fixtures read JSON into event/data/output/response objects.
- `tests/conftest.py` provides a mock Lambda context factory.
- Moto's `mock_aws()` isolates AWS calls; a fixture creates a table with the
  same string `pk` and `sk` key schema.
- `pytest-mock` patches the handler's `DDB_TABLE` and generated keys to make
  assertions deterministic.
- Handler tests assert status and decoded response; `_main` tests assert
  database state and conditional-write behavior.

These tests do not exercise deployed API Gateway, Cognito, DNS, or IAM.
`tests/integration/` and `tests/ete/` are placeholders, not a supplied live test suite.
See [Common tasks](common-tasks.md) for validation commands and schema-test guidance.

## Anatomy of mock data and schemas

Each `data/handlers/<function>/` directory pairs JSON examples with schemas:

| Files | Meaning |
| --- | --- |
| `event.json`, `event.schema.json` | API Gateway invocation envelope, including paths and request context. |
| `data.json`, `data.schema.json` | Business input used by test fixtures; tests insert its JSON into the event body where needed. |
| `response.json`, `response.schema.json` | Decoded API response body. |
| `output.json`, `output.schema.json` | Lambda proxy result, including status code and JSON-encoded body string. |

`data/common/` holds reusable API Gateway event and Lambda output schemas,
plus collection data and DynamoDB-item examples/schemas.
Some per-function schemas reference these through `file:./data/common/...`.
Run fixture-based tools from the repository root so relative paths resolve.
Schema examples do not automatically enforce validation in production handlers.

## DynamoDB single-table design

The table's composite primary key has string **partition key `pk`** and string
**sort key `sk`**. Generic names allow multiple entity types in one table.
The starter uses equal key values for each item:

```text
pk = ${{ values.collection_name }}#<uuid>
sk = ${{ values.collection_name }}#<uuid>
id = <uuid>
```

`create_keys()` generates these namespaced keys;
`get_keys_from_id(id)` reconstructs them for reads, updates, and deletes;
`get_id_from_keys(keys)` extracts the ID by splitting `pk` on `#`.
The API exposes the unprefixed ID, not the storage key.

For more entity types or relationships, design namespaces and access patterns
together, for example `customer#123` and `order#456`. Update all three helpers,
models, and tests consistently; the current extraction logic assumes a simple
`namespace#id` format. Changing key formats requires a migration plan for existing
items. No secondary indexes or relationship-query patterns are supplied.

## Repository file layout

```text
catalog-info.yaml       Backstage Component and API entities
mkdocs.yml              TechDocs site configuration
docs/                   Handbook pages
README.md               Project entry point
template.yaml           SAM infrastructure
openapi.yaml            API contract and Gateway integrations
cfn-parameters.json     Deployment-action parameter expressions
cfn-tags.json           Deployment-action tag expressions
samconfig.toml          SAM deploy defaults
Pipfile                 Local runtime/dev dependencies and scripts
pytest.ini              Pytest configuration
.cfnlintrc              CloudFormation lint configuration
.github/workflows/      main.yml and branch.yml
src/common/             Installable common package, setup.py, Makefile
src/common/common/      Shared model and utility modules
src/handlers/           Per-function code and requirements.txt
data/common/            Shared examples and schemas
data/handlers/          Per-function examples and schemas
tests/conftest.py       Shared test fixtures and import setup
tests/unit/handlers/    Per-function unit tests
tests/integration/      Integration-test placeholders
tests/ete/              End-to-end-test placeholders
```

These are generated-project paths. The template source repository keeps their
inputs separately under `skeleton/base/`, `skeleton/crud/`, `functions/crud/`,
and `pipeline/` before the scaffolder combines them.
