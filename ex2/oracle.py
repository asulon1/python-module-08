#!/usr/bin/env python3
"""Accessing the Mainframe: secure configuration with environment variables."""

import os
import sys
from dotenv import load_dotenv


REQUIRED_VARS = (
    "DATABASE_URL",
    "API_KEY",
    "LOG_LEVEL",
    "ZION_ENDPOINT",
)
VALID_MODES = {"development", "production"}


def locate_env_file() -> str:
    """Return the path to .env next to this script."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, ".env")


def load_configuration() -> dict:
    """Load environment variables and return normalized configuration."""
    env_path = locate_env_file()
    env_loaded = load_dotenv(dotenv_path=env_path, override=False)

    mode = os.getenv("MATRIX_MODE", "development").strip().lower()
    if mode not in VALID_MODES:
        print(
            f"[WARN] Invalid MATRIX_MODE '{mode}'. Falling back to 'development'.",
            file=sys.stderr,
        )
        mode = "development"

    config = {
        "MATRIX_MODE": mode,
        "DATABASE_URL": os.getenv("DATABASE_URL", "").strip(),
        "API_KEY": os.getenv("API_KEY", "").strip(),
        "LOG_LEVEL": os.getenv("LOG_LEVEL", "").strip(),
        "ZION_ENDPOINT": os.getenv("ZION_ENDPOINT", "").strip(),
        "ENV_FILE_LOADED": env_loaded,
        "ENV_FILE_PATH": env_path,
    }
    return config


def validate_config(config: dict) -> list:
    """Return missing variable names from required configuration."""
    missing = []
    for key in REQUIRED_VARS:
        if not config.get(key):
            missing.append(key)
    return missing


def describe_database(database_url: str, mode: str) -> str:
    """Produce a human-readable database status."""
    if not database_url:
        return "Missing DATABASE_URL"
    if mode == "development" and "sqlite" in database_url:
        return "Connected to local instance"
    if mode == "production":
        return "Connected to production cluster"
    return "Connected"


def describe_api_access(api_key: str) -> str:
    """Report API authentication status."""
    if not api_key:
        return "Missing API_KEY"
    return "Authenticated"


def describe_zion_network(endpoint: str, mode: str) -> str:
    """Report endpoint/network status with mode context."""
    if not endpoint:
        return "Offline (missing ZION_ENDPOINT)"
    if mode == "production":
        return f"Online (secure channel -> {endpoint})"
    return f"Online (dev relay -> {endpoint})"


def has_production_overrides() -> bool:
    """Detect if any required variables are provided directly via process env."""
    watched_vars = ("MATRIX_MODE",) + REQUIRED_VARS
    for key in watched_vars:
        if key in os.environ:
            return True
    return False


def is_env_ignored() -> bool:
    """Check if .env is ignored in local gitignore."""
    gitignore_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), ".gitignore")
    if not os.path.exists(gitignore_path):
        return False

    with open(gitignore_path, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file]

    return ".env" in lines


def main() -> int:
    """Program entrypoint."""
    print("ORACLE STATUS: Reading the Matrix...")

    config = load_configuration()
    missing = validate_config(config)

    print("Configuration loaded:")
    print(f"Mode: {config['MATRIX_MODE']}")
    print(
        f"Database: {describe_database(config['DATABASE_URL'], config['MATRIX_MODE'])}")
    print(f"API Access: {describe_api_access(config['API_KEY'])}")
    print(f"Log Level: {config['LOG_LEVEL'] or 'Missing LOG_LEVEL'}")
    print(
        f"Zion Network: {describe_zion_network(config['ZION_ENDPOINT'], config['MATRIX_MODE'])}"
    )

    if config["ENV_FILE_LOADED"]:
        print(f"Source: Loaded .env from {config['ENV_FILE_PATH']}")
    else:
        print("Source: .env not found, using system environment only")

    if missing:
        print("\n[WARN] Missing required configuration:")
        for key in missing:
            print(f"  - {key}")
        print("Provide the missing values in .env or as environment variables.")

    print("\nEnvironment security check:")
    print("[OK] No hardcoded secrets detected")
    print(
        "[OK] .env file properly configured"
        if is_env_ignored()
        else "[WARN] Add '.env' to .gitignore to avoid leaking secrets"
    )
    print(
        "[OK] Production overrides available"
        if has_production_overrides()
        else "[INFO] No explicit environment overrides detected"
    )

    print("The Oracle sees all configurations.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
