"""Helpers for running external commands through subprocess."""

import subprocess
from dataclasses import dataclass


@dataclass
class CommandOutput:
    """Minimal file-like wrapper for command output."""

    stdout: str

    def read(self) -> str:
        return self.stdout


def capture_shell(command: str) -> CommandOutput:
    """Run a shell command and return an object compatible with ``read()``."""
    result = subprocess.run(
        command,
        shell=True,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    return CommandOutput(result.stdout)


def run_shell(command: str) -> int:
    """Run a shell command and return its process exit code."""
    result = subprocess.run(command, shell=True, check=False)
    return result.returncode
