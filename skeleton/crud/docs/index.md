# Project handbook

This handbook describes the starter service generated for **${{ values.component_name }}**.
Keep it current as the service's model, infrastructure, and workflows change.

- [Features](features.md): API definition, starter code, DNS, and Cognito.
- [Creating a component](creating-a-component.md): Backstage form pages and generated outputs.
- [Configuration](configuration.md): deployment parameters, tags, and prerequisites.
- [Architecture](architecture.md): AWS resources, function and test anatomy, and repository layout.
- [CI/CD pipeline](ci-cd.md): build, deployment, and feature branches.
- [Observability](observability.md): logs, metrics, and automatic Datadog integration.
- [Common tasks](common-tasks.md): add endpoints, functions, dependencies, fixtures, and tests.

## Reading in Backstage

The component's `catalog-info.yaml` contains `backstage.io/techdocs-ref: dir:.`.
TechDocs uses the repository-root `mkdocs.yml` and the Markdown files in `docs/`.
Open the component in the catalog and select **Docs**.

The platform must enable the TechDocs frontend and backend and configure either
on-demand documentation generation or an external builder and publisher. The
builder needs MkDocs and `mkdocs-techdocs-core` for the `techdocs-core` plugin.
The generated application workflows do not build or publish documentation.
With the Backstage TechDocs CLI and its Docker prerequisites installed, preview
from the generated repository root with `techdocs-cli serve`.

The pages can also be read directly in GitHub. Application source paths shown in
backticks are relative to the generated repository root.

## Content review

Before treating this starter handbook as your service's operational reference,
review its API contract, deployment assumptions, security,
and runbooks. Template-generated documentation does not constitute human approval.
