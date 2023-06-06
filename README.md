# datadog-monitor-slos

This is a command line tool that interacts with Datadog SLOs. It provides the following features:
- Get all SLOs from a list of SLO IDs.
- Get all SLOs that match a particular tags query.
- Get all SLOs that contain at least one of the monitors in a list of monitor IDs.

All these filtering mechanisms can be combined together.

## Usage

You can type `python slos.py --help` to get help on how to use the tool:

```bash
Usage: slos.py [OPTIONS]

Options:
  -m, --monitor-ids INTEGER   Monitor IDs to get SLOs related. If not set, it
                              returns all the SLOs found.
  -i, --slo-ids TEXT          Get only SLOs with IDs specified.
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
