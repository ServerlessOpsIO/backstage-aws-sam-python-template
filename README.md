# Backstage AWS SAM Python Templates

This repository contains Backstage scaffolder templates for creating new AWS Serverless Application Model (SAM) projects in Python. It is designed to help platform teams generate consistent serverless services from Backstage, publish them to GitHub, and register them back into the catalog with standard AWS deployment patterns.

The templates in this repo cover common Python serverless use cases:

- CRUD API services
- event-driven message handlers
- scheduled event handlers

## What this repository creates

When used from Backstage, each template generates a new repository skeleton that includes:

- an AWS SAM project configured for Python
- Lambda-based serverless application code with starter tests
- supporting infrastructure definitions for API Gateway, DynamoDB, or event sources
- OpenAPI or event schema examples for the generated service
- GitHub Actions workflows for validation and deployment
- Backstage catalog metadata ready for registration

## Included templates

### 1. CRUD API template

The CRUD template creates a serverless Python API service with:

- API Gateway endpoints for create, read, update, and delete operations
- Lambda handlers for each CRUD action
- a DynamoDB table with a generic item model
- OpenAPI documentation for the generated API
- starter mock data and schema examples
- CI/CD automation for AWS SAM deployment

### 2. Message event handler template

The message event handler template creates a Python Lambda service for event-driven processing, including support for:

- Amazon EventBridge
- Amazon S3
- Amazon SNS
- Amazon SQS

It includes:

- a Lambda function with starter logic
- event payload examples and JSON schemas
- unit test scaffolding
- GitHub Actions workflows for build and deploy

### 3. Scheduled event handler template

The scheduled event handler template creates a Python Lambda service triggered on a cron, rate, or at-time schedule. It includes:

- a scheduled EventBridge trigger definition
- a starter Lambda handler
- mock event payloads and schemas
- unit tests and deployment automation

## Repository layout

- `template-crud-api.yaml` — Backstage template for the CRUD API service
- `template-message-event-handler.yaml` — Backstage template for message-based event handlers
- `template-scheduled-event-handler.yaml` — Backstage template for scheduled event handlers
- `skeleton/` — source files copied into a generated project
- `skeleton/base/` — shared Python SAM project configuration and base test structure
- `skeleton/crud/` — CRUD API project files and OpenAPI metadata
- `skeleton/event_handler/` — event-driven Lambda project files
- `functions/` — reusable Lambda function templates and starter code for generated projects
- `pipeline/` — GitHub Actions workflow templates used by generated repositories

## Included technology

These generated projects are built around standard AWS and Python tooling:

- AWS SAM for infrastructure-as-code and deployment
- AWS Lambda for serverless execution
- API Gateway for HTTP-based APIs
- DynamoDB for persistence in the CRUD template
- Python 3.13 or 3.14 for application runtimes
- pytest for unit tests
- GitHub Actions for CI/CD

## Typical use in Backstage

The scaffolder prompts for component metadata such as:

- component name and description
- owning group
- domain and system
- deployment environment
- target AWS account
- API hostname, path prefix, and collection name for CRUD APIs
- event source details for message and scheduled handlers

It then:

1. fetches the related Backstage catalog entities,
2. copies the appropriate project skeleton,
3. adds function-specific starter code and schemas,
4. creates the deployment pipeline files,
5. publishes the repository to GitHub,
6. registers the generated component back in Backstage.

## Generated project structure

Each generated project is intentionally opinionated and ready for a real service to be customized. Typical generated content includes:

- Python Lambda handlers under `src/handlers/`
- shared model and utility modules under `src/common/`
- test scaffolding under `tests/`
- AWS SAM templates for the service definition
- OpenAPI or event examples for the generated interface
- deployment configuration for AWS SAM and GitHub Actions

## Requirements

Before using these templates in a Backstage setup, make sure the following are available:

- Backstage with the Scaffolder plugin enabled
- GitHub publisher integration configured for repository creation
- catalog entities for domain, system, owner, environment, and cloud account
- AWS account and target deployment configuration
- AWS SAM tooling available in the generated project pipeline

## Next steps

After generating a project from one of these templates:

- adapt the starter model and business logic to your real domain
- update Lambda handlers and event schemas for your service behavior
- customize API routes, event sources, and permissions in the generated SAM template
- adjust deployment parameters and environment configuration for your AWS environment

This repository is a good starting point for teams standardizing Python-based serverless services through Backstage with repeatable AWS deployment patterns.
