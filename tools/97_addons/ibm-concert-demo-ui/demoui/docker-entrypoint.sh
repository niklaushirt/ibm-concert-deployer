#!/bin/sh
set -eu

if [ -z "${DJANGO_SECRET_KEY:-}" ]; then
    secret_key_file="${DJANGO_SECRET_KEY_FILE:-/tmp/demoui/django-secret-key}"

    if [ ! -s "$secret_key_file" ]; then
        secret_key_directory="$(dirname "$secret_key_file")"
        mkdir -p "$secret_key_directory"
        umask 077
        python_command="python"
        if ! command -v "$python_command" >/dev/null 2>&1; then
            python_command="python3"
        fi
        "$python_command" -c 'import secrets; print(secrets.token_urlsafe(64))' > "$secret_key_file"
    fi

    DJANGO_SECRET_KEY="$(head -n 1 "$secret_key_file")"
    if [ -z "$DJANGO_SECRET_KEY" ]; then
        echo "DJANGO_SECRET_KEY_FILE does not contain a usable key" >&2
        exit 1
    fi
    export DJANGO_SECRET_KEY

    echo "DJANGO_SECRET_KEY was not supplied; using a private per-container key." >&2
fi

exec "$@"
