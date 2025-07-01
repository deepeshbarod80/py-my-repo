
1. CloudWatch Logs:
# Log Management:
`create_log_group()`: Creates a new log group.
`create_log_stream()`: Creates a new log stream within a log group.
`delete_log_group()`: Deletes a log group.
`delete_log_stream()`: Deletes a log stream.
`describe_log_groups()`: Lists log groups.
`describe_log_streams()`: Lists log streams within a log group.

# Log Data:
`put_log_events()`: Sends log data to a log stream.
`get_log_events()`: Retrieves log events from a log stream.
`start_query()`: Starts a query to analyze log data with CloudWatch Logs Insights.
`get_query_results()`: Gets the results of a CloudWatch Logs Insights query.
`start_live_tail()`: Starts a live tail to stream log events in real-time.

# Subscription Filters:
`put_subscription_filter()`: Creates a filter to route log events to other services (e.g., Lambda).
`delete_subscription_filter()`: Deletes a subscription filter.
`describe_subscription_filters()`: Lists subscription filters.

# Export Tasks:
`create_export_task()`: Creates a task to export log data to S3.
`cancel_export_task()`: Cancels an export task.
`describe_export_tasks()`: Lists export tasks. 

---

2. CloudWatch (General):
# Metrics:
`put_metric_data()`: Sends custom metrics to CloudWatch.
`get_metric_data()`: Retrieves metric data.
`get_metric_statistics()`: Retrieves statistics for a metric.

# Alarms:
`put_metric_alarm()`: Creates or updates a metric alarm.
`delete_alarms()`: Deletes alarms.
`describe_alarms()`: Describes alarms.

# Dashboards:
`put_dashboard()`: Creates or updates a dashboard.
`get_dashboard()`: Retrieves a dashboard.
`delete_dashboards()`: Deletes dashboards.

# Events (EventBridge):
`put_events()`: Publishes events to CloudWatch Events.
`put_rule()`: Creates or updates a rule that triggers actions based on events.
`put_targets()`: Adds targets to a rule (e.g., Lambda functions). 

# CloudWatch Synthetics:
`create_group()`: Creates a group of canaries.
`delete_group()`: Deletes a group of canaries.
`describe_group()`: Describes a group of canaries.
`create_canary()`: Creates a canary.
`delete_canary()`: Deletes a canary.
`describe_canary()`: Describes a canary.
`run_canary()`: Runs a canary test.