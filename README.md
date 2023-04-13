# datadog-monitor-slos

This is a command line tool that fetches all the SLOs from Datadog that contain a particular Monitor ID.

## Usage

You can type `python slos.py --help` to get help on how to use the tool:

```bash
Usage: slos.py [OPTIONS]

Options:
  -m, --monitor-id INTEGER    Monitor ID to get SLOs related. If not set, it
                              returns all the SLOs found.  [default: -1]
  --datadog-api-key TEXT      Datadog API key.  [env var:
                              SLOS_DATADOG_API_KEY; required]
  --datadog-app-key TEXT      Datadog APP key.  [env var:
                              SLOS_DATADOG_APP_KEY; required]
  -q, --tags-query TEXT       Datadog tags query for querying the SLOs.  [env
                              var: SLOS_TAGS_QUERY]
  -p, --pretty / --no-pretty  Pretty output.  [env var: SLOS_PRETTY; default:
                              no-pretty]
  -v, --debug / --no-debug    Debug logging.  [env var: SLOS_DEBUG; default:
                              no-debug]
  --help                      Show this message and exit.
```
