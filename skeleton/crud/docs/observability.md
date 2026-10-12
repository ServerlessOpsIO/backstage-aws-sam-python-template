# Observability

## Function logging

Handlers use AWS Lambda Powertools `Logger(utc=True)` and
`@LOGGER.inject_lambda_context` for structured logs with invocation context.
`POWERTOOLS_SERVICE_NAME` is set to the CloudFormation stack name.
CloudWatch receives Lambda logs in `/aws/lambda/<physical-function-name>`;
find the physical name in the stack resources or Lambda console.

Get and Delete log the full incoming event at **INFO**, so those entries are
emitted at the logger's default INFO level. Create and Upsert log events at
**DEBUG**, and all four handlers log outgoing proxy outputs at DEBUG.
For temporary debugging, configure the Powertools `LOG_LEVEL` environment
variable through SAM and redeploy, after sanitizing the logged data.
Add meaningful, sanitized business logs as the service evolves.

Full API events can contain authorization headers, personal information, and
request bodies. Redact or remove full-event logging **before production use**,
including the existing INFO calls, and sanitize outputs before enabling DEBUG.
Never log tokens, credentials, or app-client secrets.
The template does not specify Lambda log-group retention; set an appropriate
retention policy for your service.

## API Gateway logging

`RestApiLogGroup` creates `/aws/api-gateway/<stack-name>` with **seven-day**
retention. Access logs include extended request ID, source IP, caller/user,
request time, HTTP method/resource path/protocol, status, response length, and
request ID.

Method settings enable INFO execution logging for all paths and methods,
enable detailed metrics, and set `DataTraceEnabled: false` so full request and
response payload tracing is not enabled by the template. Execution logs are
separate from the configured access log group.

API Gateway needs the account/region-level CloudWatch logging role configured
for REST APIs. This template does not define `AWS::ApiGateway::Account` or that
logging role; `RestApiIamRole` grants DynamoDB query access and is **not** a
CloudWatch logging role. Confirm the platform has configured API logging.

Use access logs for route/status-level investigation and Lambda logs for handler
behavior. API Gateway request IDs and Lambda `aws_request_id` are different
identifiers; record both explicitly in sanitized application logs if you need
cross-service correlation.

## Metrics

AWS provides standard Lambda metrics such as Invocations, Errors, Duration,
Throttles, and ConcurrentExecutions. API Gateway metrics include Count, Latency,
IntegrationLatency, 4XXError, and 5XXError; the template enables detailed method
metrics. DynamoDB also exposes capacity, throttling, and latency metrics.

Filter by the actual deployed function/table names and API stage, especially
when investigating branch deployments. Watch error rates and throttles alongside
latency, not just invocation counts.

The starter does not emit custom Powertools business metrics, configure alarms
or dashboards, or enable X-Ray tracing. Add these intentionally based on your
service's reliability targets.

## Availability in Datadog

Logs and metrics can be available in Datadog **when the platform's AWS
integration and log forwarding are configured**. This repository does not
provision a Datadog integration, forwarder, Lambda extension, log subscriptions,
dashboards, or Datadog credentials.

To make logs and metrics available in Datadog:

1. Enable AWS metric collection for Lambda, API Gateway, and DynamoDB in the
   deployment account/region.
2. Forward both Lambda log groups and the API Gateway access/execution log groups
   using the organization's approved forwarding mechanism.
3. Apply consistent service, environment, and branch tags to distinguish stacks.
   CloudFormation's `org:*` tags and Powertools service names do not by themselves
   guarantee Datadog's service/environment mapping.
4. Verify a sanitized test log and recent invocation/API metrics arrive in Datadog.

In Datadog Logs Explorer, locate the deployed service or function/log-group
identifier and narrow the time range, then search the request ID from an error.
Use Metrics Explorer to inspect the imported AWS metrics and account/region/stage
dimensions. Exact field names and tags depend on the integration's pipelines.
If data is missing, first confirm it exists in CloudWatch, then check collection
permissions, subscriptions, integration filters, and forwarding errors.

## Request investigation checklist

1. Note the timestamp, HTTP method, route, status, and any returned request ID.
2. Find the API Gateway access entry and determine whether the failure happened
   during authorization/validation or during Lambda integration.
3. Inspect the corresponding Lambda invocation and database errors, without
   copying sensitive payloads into tickets.
4. Compare error/latency/throttling metrics with recent deployments.
5. Check Datadog ingestion separately if CloudWatch data is present but missing
   from Datadog.
