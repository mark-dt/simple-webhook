# simple_webhook extension

A Dynatrace Extension Framework 2.0 (Python, remote) extension that runs a small
Flask listener and logs the JSON payloads posted to it.

## Endpoints

| Method | Path      | Description                                  |
| ------ | --------- | -------------------------------------------- |
| `POST` | `/upload` | Accepts a JSON body and logs it. `400` if the body is not valid JSON. |
| `GET`  | `/info`   | Liveness probe.                               |

The listener binds `0.0.0.0` on the configured port (default `9000`).

## Developing

1. Clone this repository
2. Install dependencies with `pip install -e ".[dev]"`
3. Copy `activation.example.json` to `activation.json` and fill in your tenant
   URL, API token, and port. `activation.json` is git-ignored — never commit it.
4. Increase the version under `extension/extension.yaml` after modifications

## Running

* `dt-sdk run`

Uses `activation.json` for simulation only.

## Building and signing

* `dt-sdk build -e manylinux2014_x86_64`

## Structure

| Path                            | Purpose                                                     |
| ------------------------------- | ----------------------------------------------------------- |
| `simple_webhook/`               | Python code for the extension                                |
| `extension/extension.yaml`      | Extension definition for the EF2 framework                   |
| `extension/activationSchema.json` | Activation settings schema shown in the Dynatrace UI        |
| `setup.py`                      | Dependency and other Python metadata                         |
| `activation.example.json`       | Template for the local, git-ignored `activation.json`        |

## Known gaps

`activation.json` / the activation schema collect a `tenant_url` and an API
token described as needing the `logs.ingest` scope, but the listener does not
currently forward anything to Dynatrace — it only logs received payloads. The
credentials are collected for a forwarding path that is not yet implemented.
