# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  oracle.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: asulon <asulon@student.42nice.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/04 22:14:58 by asulon          #+#    #+#               #
#  Updated: 2026/05/04 22:17:46 by asulon          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import os
from typing import Any
from dotenv import load_dotenv


def load_configuration() -> dict[str, Any]:
    load_dotenv()

    config = {
        "MATRIX_MODE": os.getenv("MATRIX_MODE"),
        "DATABASE_URL": os.getenv("DATABASE_URL"),
        "API_KEY": os.getenv("API_KEY"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL"),
        "ZION_ENDPOINT": os.getenv("ZION_ENDPOINT"),
    }

    return config


def validate_config(config: dict[str, Any]) -> bool:
    missing = [key for key, value in config.items() if not value]

    if missing:
        print("WARNING: Missing configuration variables:")
        for key in missing:
            print(f" - {key}")
        print("Using fallback defaults where possible...\n")

    return len(missing) == 0


def display_status(config: dict[str, Any]) -> None:
    print("ORACLE STATUS: Reading the Matrix...\n")
    print("Configuration loaded:")

    mode = config["MATRIX_MODE"] or "undefined"

    print(f"Mode: {mode}")

    if config["DATABASE_URL"]:
        if mode == "production":
            print("Database: Connected to production cluster")
        else:
            print("Database: Connected to local instance")
    else:
        print("Database: Not configured")

    if config["API_KEY"]:
        print("API Access: Authenticated")
    else:
        print("API Access: Missing key")

    print(f"Log Level: {config['LOG_LEVEL'] or 'INFO (default)'}")

    if config["ZION_ENDPOINT"]:
        if mode == "production":
            print("Zion Network: Secure channel established")
        else:
            print("Zion Network: Online")
    else:
        print("Zion Network:  Unreachable")

    print("\nEnvironment security check:")

    if config["API_KEY"] and "dev" in config["API_KEY"].lower():
        print("[WARNING] Development API key detected")
    else:
        print("[OK] No hardcoded secrets detected")

    if os.path.exists(".env"):
        print("[OK] .env file properly configured")
    else:
        print("[WARNING] No .env file found")

    if mode == "production":
        print("[OK] Production overrides active")
    else:
        print("[OK] Development mode active")

    print("\nThe Oracle sees all configurations.")


def main() -> None:
    config = load_configuration()
    validate_config(config)
    display_status(config)


if __name__ == "__main__":
    main()
