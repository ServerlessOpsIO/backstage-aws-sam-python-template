# backstage-aws-sam-python-template

Backstage software templates for bootstrapping AWS SAM Python serverless services.

## Included templates

This repository provides three Backstage `scaffolder.backstage.io/v1beta3` templates:

- `template-crud-api.yaml` — creates a serverless CRUD API using API Gateway, Lambda, DynamoDB, OpenAPI, and CI/CD workflows.
- `template-message-event-handler.yaml` — creates an event-driven Lambda service for message/event sources (EventBridge, S3, SNS, SQS) with optional destinations.
- `template-scheduled-event-handler.yaml` — creates a scheduled Lambda service using EventBridge schedule expressions (`cron`, `rate`, `at`).

## What generated projects include

Depending on template selection, generated repositories include:

- AWS SAM project structure
- Python Lambda starter code
- Unit/integration test scaffolding
- Example schemas/mock payloads
- GitHub Actions workflows for build/deploy
- Backstage `catalog-info.yaml`

## Repository layout

- `template-*.yaml` — Backstage template definitions and user input forms
- `skeleton/base` — common files shared by all generated projects
- `skeleton/crud` — CRUD-specific generated files (including OpenAPI and README guidance)
- `skeleton/event_handler` — event-handler-specific generated files (including README guidance)
- `functions/` — reusable function-level source scaffolding
- `pipeline/` — reusable GitHub Actions workflow templates

## README examples used by generated projects

The generated service READMEs are scaffolded from:

- `skeleton/crud/README.md`
- `skeleton/event_handler/README.md`

These files contain the “new project getting started” guidance for teams after a repository is created.
