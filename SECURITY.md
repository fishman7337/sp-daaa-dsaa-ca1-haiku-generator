# Security Policy

## Supported Version

This coursework project currently supports the latest version on the main branch.
Security fixes should target that branch first.

## Reporting a Vulnerability

Do not publish exploit details in public issues. For coursework review, report
concerns through the appropriate Singapore Polytechnic module or school channel.
For local maintenance, contact the project maintainer directly with:

- A concise description of the issue.
- Steps to reproduce.
- Affected files or commands.
- Suggested mitigation, if known.

## Security Controls

The repository includes:

- Ruff linting with selected security rules.
- Bandit static security scanning.
- Pip-audit dependency vulnerability checks.
- GitHub CodeQL analysis.
- `.env.example` without secrets or credentials.

The application does not require network access, credentials, or external model
APIs at runtime.
