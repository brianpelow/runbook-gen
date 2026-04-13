# runbook-gen

> Auto-generates operational runbooks from code, alerts, and incident history using AI.

![CI](https://github.com/brianpelow/runbook-gen/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.12+-green.svg)

## Overview

`runbook-gen` eliminates the most neglected part of operational readiness —
writing runbooks. It reads your code comments, alert definitions, and past
incident data and generates structured operational runbooks using Claude.

Built for engineering teams in regulated financial services, fintech, and
manufacturing where runbooks are a compliance requirement under frameworks
like FFIEC, SOX, and IEC 62443 — not just operational good practice.

## Quick start

```bash
pip install runbook-gen

# Generate a runbook from a service directory
runbook-gen generate src/payments_service/ --output runbooks/

# Generate from an alert definition file
runbook-gen from-alerts alerts/critical.yml --output runbooks/

# Generate from past incident data
runbook-gen from-incident incidents/INC-2024-047.md --output runbooks/

# Export a runbook to Confluence
runbook-gen export runbooks/payments-runbook.md --target confluence
```

## Commands

| Command | Description |
|---------|-------------|
| `runbook-gen generate` | Generate runbook from a service directory |
| `runbook-gen from-alerts` | Generate from alert definition files |
| `runbook-gen from-incident` | Generate from past incident markdown |
| `runbook-gen export` | Export runbook to Markdown or Confluence |
| `runbook-gen validate` | Validate a runbook against compliance standards |

## Generated runbook format

```markdown
# Service Name — Operational Runbook

## Service overview
## On-call contact
## Architecture diagram
## Common alerts and responses
## Step-by-step remediation procedures
## Escalation paths
## Rollback procedures
## Compliance notes
## Revision history
```

## Configuration

| Variable | Description | Required |
|----------|-------------|----------|
| `ANTHROPIC_API_KEY` | Claude API key for generation | Yes |
| `CONFLUENCE_URL` | Confluence base URL for export | No |
| `CONFLUENCE_TOKEN` | Confluence API token | No |
| `RUNBOOK_INDUSTRY` | Industry context (fintech/manufacturing) | No |

## Industry context

In regulated environments, runbooks serve as evidence of operational controls.
`runbook-gen` produces runbooks aligned with:

- **Fintech**: FFIEC IT examination handbooks, SOX ITGC controls, PCI-DSS
- **Manufacturing**: IEC 62443 operational procedures, ISO 9001 work instructions

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Apache 2.0 — see [LICENSE](LICENSE).