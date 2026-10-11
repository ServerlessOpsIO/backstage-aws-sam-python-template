# Creating a component via Backstage

Choose **Create** in Backstage and select **AWS Serverless CRUD API (Python)**.
The platform needs GitHub publishing, catalog registration, the template's
custom form fields/actions, and catalog entities for the choices below.

## Page 1: Component Info

| Input | Purpose |
| --- | --- |
| Name | Unique component name; becomes the repository name, catalog entity name, and default SAM stack name. |
| Description | Describes the repository, component, and SAM application. |
| Owner | Owning group, selected from your groups; fetched from the catalog and recorded in the GitHub repository's `owner` custom property. |
| Domain | Catalog domain; used for project metadata, deployment parameters, tags, and GitHub custom properties. |
| System | Catalog system filtered by the chosen domain; used in catalog relationships, parameters, tags, and GitHub custom properties. |
| Environment | Catalog environment filtered by the chosen system; narrows the cloud-account picker. |
| Account ID | Catalog cloud-account resource related to the environment; its `metadata.title` supplies the repository's `DEPLOYMENT_ACCOUNT_ID` secret. Confirm that title contains the AWS account ID. |

Hidden defaults are lifecycle `production`, namespace `default`, and GitHub
organization `ServerlessOpsIO`. Namespace is collected but is not currently
passed into generated catalog metadata.

Review ownership after creation: the current template passes the **system name**
as `owner_name`, so the generated Component and API `spec.owner` use that name
as a group reference, not the selected Owner. Confirm or correct `catalog-info.yaml`
to reference the intended owning group.

Choosing an Environment does not configure a matching GitHub environment:
the generated workflows both explicitly use `production`.

## Page 2: Software configuration

| Input | Purpose |
| --- | --- |
| Hostname | Fully qualified API DNS name; supplies the deployment hostname, certificate, custom domain, and DNS record. |
| Path Prefix | Prefix before the collection path, such as `/v1`; defaults to `/v1`. Include the leading slash and avoid a trailing slash. |
| Collection Name | Collection path segment and source/model naming input. Use a name valid in Python module names, for example `thing`; punctuation such as hyphens will produce invalid Python imports. |
| API Description | Description in the OpenAPI document and Backstage API entity. |
| Python Version | Selects 3.13 or 3.14 (default 3.14) for Lambda, local dependency metadata, and CI's Python setup. |

For example, prefix `/v1` and collection `thing` produce `/v1/thing` and
`/v1/thing/{id}`. These are URL paths, not DynamoDB table names.

## Page 3: Copilot Cloud Agent

**Launch Copilot agent?** defaults to false. Leaving it disabled generates the
service without launching an agent.

If enabled, supply a non-empty **Agent prompt** describing the work to perform
in the new repository and authorize the GitHub credential request. The
`SoRequestUserCredentials` field requests credentials under `USER_GITHUB_TOKEN`
with the additional `read:user` scope. The conditional
`github:copilot:agent:launch` action launches the agent after publication and
catalog registration. This requires platform support and appropriate GitHub
access. Do not put secrets in the prompt.

## Review and create

Review the form summary, especially repository name, account, hostname, and
collection name, before submitting. The scaffolder then:

1. Fetches the selected owner, domain, system, and account catalog entities.
2. Copies shared files, CRUD infrastructure and handbook, starter functions and
   tests, and GitHub Actions workflows.
3. Publishes a **public** repository with `main` as the default branch and sets
   `DEPLOYMENT_ACCOUNT_ID`.
4. Registers the generated Component and OpenAPI API entity in Backstage.
5. Optionally launches Copilot.

The results link to the repository, `catalog-info.yaml`, catalog component,
and optional agent task. Default branch protection is disabled and the required
approving review count is zero in the publisher configuration; apply your team's
review policy before development.

## After creation

- Confirm catalog ownership and relationships.
- Complete [deployment configuration](configuration.md) before assuming the
  initial push can deploy successfully.
- Review [branch deployment isolation](ci-cd.md) before pushing additional branches.
- Open the component's **Docs** tab, or read `docs/index.md` in the repository.
- Adapt the model and contract using [Common tasks](common-tasks.md), and request
  human review of the generated handbook.
