# Safe installation and authentication

This derivative intentionally does not execute installers. Use the official ElevenLabs website or a reviewed, fixed-version official SDK or CLI.

Official SDK choices are the ElevenLabs JavaScript SDK in the elevenlabs GitHub organization, or its Python SDK. Confirm the publisher, exact version, package integrity and local project destination before installation. Keep a lockfile and review dependency installation scripts before enabling them. Do not substitute similarly named third-party packages.

The official CLI supports interactive authentication. The user completes login privately; the agent does not extract, reveal, transfer or persist credentials. Authentication is separate from authorization to generate paid content.

For JavaScript, instantiate ElevenLabsClient using the user's privately configured process environment; for Python, instantiate ElevenLabs in the same manner. Do not insert secrets into source code or command-line arguments. Do not read credential files to discover a key.

After installation, test version and help output first. A successful help command proves only local installation, not account access. An approved bounded generation is required to validate service connectivity, output and commercial rights.
