# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  construct.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: asulon <asulon@student.42nice.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/04/23 16:25:35 by asulon          #+#    #+#               #
#  Updated: 2026/04/24 17:48:50 by asulon          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import sys
import os


def main():
    is_virtual = (sys.prefix != sys.base_exec_prefix or
                  'VIRTUAL_ENV' in os.environ)

    matrix_status = ("Welcome to the construct" if is_virtual
                     else "You're still plugged in")

    print(f"MATRIX STATUS: {matrix_status}\n")
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {os.environ.get('VIRTUAL_ENV_PROMPT')}")

    if not is_virtual:
        print("\nWARNING: You're in the global environment!\n"
              "The machines can see everything you install.\n")
        print("To enter the construct, run:\n"
              "python -m venv matrix_env\n"
              "source matrix_env/bin/activate # On Unix\n"
              "matrix_env/Scripts/activate # On Windows\n")
        print("Then run this program again")
    else:
        for path in sys.path:
            if "site-packages" in path:
                package_path = path
                break

        print(f"Environment Path: {sys.prefix}\n")
        print("SUCCESS: You're in an isolated environment!\n"
              "Safe to install packages without affecting the global system\n")
        print(f"Package installation path: {package_path}\n")


if __name__ == "__main__":
    main()
