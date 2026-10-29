# backstage-aws-sam-python-template Constitution

## Core Principles

### I. Every Option Combination Renders Correctly

- Every supported combination of template inputs MUST render a complete, valid project.
  A form choice MUST NOT produce a broken file or an invalid project.
- Content declared inside a `{% if %}` block MUST NOT be referenced outside that block.
- Every variable used by a skeleton, including in file and directory names, MUST be passed in
  the `fetch:template` `values` for every template that renders it.
- Rendered JSON and YAML MUST remain valid for every supported option combination, including
  conditional commas and indentation.
- In skeletons read by GitHub Actions, Actions expressions `${{ }}` MUST be wrapped in
  `{% raw %}...{% endraw %}` so template rendering preserves them.
- Generated projects MUST pass their generated pipeline's validation, build, and test steps
  without hand edits.
- A change to a skeleton or an option MUST be verified by rendering every affected option
  combination, not only the default path.

These rules make each advertised template choice dependable from form submission through
generated-pipeline execution.

### II. The Catalog Drives Inputs

- Ownership and placement MUST use catalog pickers with `allowArbitraryValues: false`:
  owner from `MyGroupsPicker`, then Domain, System filtered by Domain, and Environment and
  cloud account filtered by the preceding selections.
- Existing catalog entities MUST be selected through catalog pickers, not free-text fields.
- Values read from `catalog:fetch` MUST belong to the referenced entity. If the `entityRefs`
  order changes or an entity is added, every expression reading a result by index MUST be
  updated.
- Implicit catalog contracts MUST be documented next to their use. This includes the cloud
  account ID being read from the resource title and the component name also serving as the
  repository name.

Catalog-backed inputs keep generated repositories attached to valid organizational ownership
and deployment resources.

### III. Published Repositories and Entities Are Predictable

- The three project templates are `template-crud-api.yaml` (CRUD API),
  `template-message-event-handler.yaml` (message-driven Lambda handler), and
  `template-scheduled-event-handler.yaml` (scheduled Lambda handler). Each creates a new
  GitHub repository and a Backstage Component; the CRUD template also creates an API entity.
- `component_name` MUST be the lowercase name used for both the GitHub repository and generated
  Component; these templates add no suffix. The GitHub organization MUST come from a hidden
  `github_org` parameter defaulting to `ServerlessOpsIO`, never from a hard-coded step or
  skeleton value.
- Every generated `catalog-info.yaml` MUST set `owner`, `system`, `lifecycle`, and the
  `github.com/project-slug` annotation. Its entity `spec.type` MUST describe the entity the
  template creates, and catalog relations MUST represent APIs exposed or entities depended
  upon. The CRUD Component MUST provide its generated API entity.
- Project templates MUST publish with `main` as the default branch, set repository custom
  properties for domain, system, and owner from catalog selections, and register
  `/catalog-info.yaml` at the repository root.
- All project templates MUST use the same repository visibility and branch-review settings.
  The current standard is public visibility, no default-branch protection, and zero required
  approving reviews; any difference MUST be explained in that template.
- Workflow templates are not present in this repository. If one is added, it MUST work on a
  named branch, never push to or merge into the default branch, open a pull request, and build
  on its earlier branch when rerun with the same input.

Predictable naming and catalog relations make repository creation and registration reproducible.

### IV. Steps Are Ordered, Optional, and Fail Safely

- Project-template steps MUST follow this order: fetch catalog entities; render project
  skeletons and starter code; render the pipeline; add optional starters; publish; register;
  then run optional steps that act on the published repository or external services.
- Optional steps MUST be disabled unless selected, guarded by `if:`, and expose or require
  their inputs only when enabled.
- Steps calling external services—including Copilot, Spec Kit, and Datadog—MUST run after
  catalog registration so a failure does not leave an unregistered project.
- Inline shell in any future workflow-template step MUST begin with `set -eu` and stop on
  unexpected state.
- Comments MUST explain non-obvious step behavior next to the step, including explicit values,
  external-resource matching, and catalog-filter dependencies.

Fixed ordering limits partial creation, and opt-in integrations avoid unexpected external
actions.

### V. Credentials and Secrets Stay Out of Templates

- Secrets and account-specific values MUST reach generated repositories only through
  scaffolder secrets and the `secrets` input of `publish:github`.
- Secrets MUST NOT be written into skeleton files, template defaults, or this repository.
  Skeletons MUST refer to secrets by name for generated pipelines to resolve at runtime.
- Actions performed on behalf of the user—including Copilot, Spec Kit, and work on an existing
  repository—MUST use the user's GitHub credentials requested with
  `SoRequestUserCredentials` into `USER_GITHUB_TOKEN`, with only the required scopes.
- Tokens MUST NOT be written to files, Git remotes, logs, or pull-request text.
- Initial commits MUST be authored as the user running the template, using the name and email
  in that user's catalog profile.

Keeping credentials in the appropriate runtime secret channels prevents leakage and preserves
user attribution.

### VI. The Form Is Honest and Templates Are Consistent

- Parameter titles and descriptions, including hidden fields, MUST accurately describe their
  behavior. Defaults MUST be values a user can reasonably accept.
- Fields applicable only to particular choices MUST be shown and required through JSON Schema
  `dependencies`, and only when applicable.
- An enum option MUST NOT be offered unless the template renders a working project for it.
- Step IDs and names MUST describe the action performed.
- Templates MUST share the same first parameter page, metadata conventions for owner, tags, and
  description format, and `publish:github` settings. A shared-field change MUST be applied to
  every applicable template unless the difference is explained.
- Every template's `output.links` MUST link to what it creates: the repository, catalog entity,
  and any agent task or external resource created by an optional step.

Consistent, accurate forms make template behavior understandable and reduce configuration drift.

## Scaffolder Constraints and Optional Integrations

- This repository contains Backstage project templates that render Python AWS SAM services
  using files from `skeleton/base`, `skeleton/crud`, `skeleton/event_handler`, `functions/`,
  and `pipeline/.github/workflows`.
- Supported outputs are a CRUD API backed by API Gateway, Lambda, and DynamoDB; a message
  handler for EventBridge, S3, SNS, or SQS; and a scheduled Lambda handler supporting cron,
  rate, or at-time schedules.
- Optional actions currently include Copilot agent launch and Spec Kit initialization for
  generated repositories, plus baseline Datadog alarms in the CRUD template. Optional steps
  MUST obey Principle IV. The generated applications' infrastructure and application design
  are governed by their own project standards, not this constitution.
- A change to template inputs, generated files, required catalog entities, required secrets,
  required scaffolder actions, or other prerequisites MUST update the repository `README.md`
  in the same change. A new or changed scaffolder action MUST name the action and providing
  Backstage module in that README.
- Generated, operating-system, and editor files—including `.DS_Store`, `__pycache__`, and
  `node_modules`—MUST NOT be committed.

## Development Workflow and Quality Gates

- Before merge, affected templates MUST be run through the Backstage template editor dry run.
  Every affected option combination MUST be rendered and checked against Principle I.
- Changes to publishing, registration, optional external steps, or workflow-template Git
  behavior MUST be exercised by a real run against a test component or sandbox.
- The pull request MUST list the checks and runs performed.
- Work MUST use `feature/` or `bug/` branches referencing an issue number when one exists,
  conventional-commit messages such as `feat:`, `fix:`, or `refactor:`, and pull-request
  merges.

These quality gates verify both generated output and interactions with Backstage and external
services before a change is merged.

## Governance

This constitution supersedes conflicting conventions in this repository. Every specification,
plan, and pull request MUST check compliance with it. Amendments MUST be made in the same change
that introduces a new rule and MUST include a Sync Impact Report for review; remove the report
before committing the amended constitution. Amendments require review and approval through a
pull request.

Versioning follows semantic versioning: MAJOR removes or incompatibly redefines a principle;
MINOR adds a principle or materially expands a section; PATCH clarifies wording without
changing requirements.

**Version**: 1.0.0 | **Ratified**: 2026-10-29 | **Last Amended**: 2026-10-29
