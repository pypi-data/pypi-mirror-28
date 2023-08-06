# Installation 
`pip install stackdriver-error-reporting`

# Usage
```
from stackdriver_error_reporting import StackdriverReporter

logger = StackdriverReporter(service_name='some-python-service', service_version='1.0.0')

try:
    raise ValueError("Wrong value!!")
except ValueError:
    logger.log_error()
```

# More on reporting errors to Stackdriver Error Reporting
[Stackdriver Logging](https://console.cloud.google.com/logs/viewer) picks up almost everything that is printed to `stdout` and `stderr` within the cluster by default, but not every error ends up in [Stackdriver Error Reporting](https://console.cloud.google.com/errors) by default.

In order to enforce this behaviour, we need to log messages according to a certain structure ([read more here](https://cloud.google.com/error-reporting/docs/formatting-error-messages)):
```
{
  "eventTime": string, // Seems superfluous, is inferred by the logging agents
  "serviceContext": {
    "service": string,     // Required
    "version": string
  },
  "message": string,       // Required. Should contain the full exception
                           // message, including the stack trace.
  "context": {
    "httpRequest": {
      "method": string,
      "url": string,
      "userAgent": string,
      "referrer": string,
      "responseStatusCode": number,
      "remoteIp": string
    },
    "user": string,
    "reportLocation": {    // Required if no stack trace in 'message'.
      "filePath": string,
      "lineNumber": number,
      "functionName": string
    }
  }
}
```
**Note:** Log JSON payloads without any pretty printing and unnecessary whitespaces/newlines as Stackdriver cannot handle this properly.
# Recommended message structure

## Service context

The name and version of the service. You can pass them yourself as an object (see example) or by setting the `SERVICE_VERSION` and `SERVICE_NAME` environment variables.

In [Stackdriver Error Reporting](https://console.cloud.google.com/errors), these values will be reflected in the `Seen in` column. This also facilitates the automatic grouping of errors.

## message
Pass the error message AND the full stack trace in here. In `JavaScript`, this is the `stack` property found on errors. In Python, you can use the `traceback` module and cast the trace to a string:
```
stacktrace = traceback.format_exc()
```
If you don't have a stack trace, include a sibling property called `reportLocation` (such as given in the example above).

## Additional fields
You can attach more information to the message, for example by attaching an additional hash or object called `customProperties` or whatever. They will not be used by Stackdriver when aggregating errors, but can still be examined in Stackdriver Logging in the `jsonPayload` property. 

# Payload validation
You can use the `gcloud` CLI to push a JSON payload to Stackdriver Logging if you wish to validate its structure and that it properly ends up in Error Reporting:

```
gcloud beta logging write --payload-type=json test-errors-log '{"serviceContext": {"version": "1.1.4", "service": "recommender"}, "message": "Traceback (most recent call last):\n  File \"Logger.py\", line 36, in <module>\n    int(\"a\")\nValueError: invalid literal for int() with base 10: 'a'\n", "severity": "error"}'
```

You might have to install some beta tools for Google Cloud SDK (in which case you'll be prompted to do so anyway).
