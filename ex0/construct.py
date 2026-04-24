# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  construct.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: asulon <asulon@student.42nice.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/04/23 16:25:35 by asulon          #+#    #+#               #
#  Updated: 2026/04/24 22:59:16 by asulon          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import sys
import os


def main():
    is_virtual = (sys.prefix != sys.base_exec_prefix or
                  'VIRTUAL_ENV' in os.environ)

    if not is_virtual:
        print("MATRIX STATUS: You're still plugged in")
        print(f"Current Python: {sys.executable}")
        print("Virtual Environment: None detected")
        print("\nWARNING: You're in the global environment!")
        print("The machines can see everything you install.")
        print("\nTo enter the construct, run:")
        print("python -m venv matrix_env")
        print("source matrix_env/bin/activate  # On Unix")
        print("matrix_env\\Scripts\\activate      # On Windows")
        print("\nThen run this program again.")
    else:
        for path in sys.path:
            if "site-packages" in path:
                package_path = path
                break

        venv_path = sys.prefix
        venv_name = os.path.basename(venv_path)
        print("MATRIX STATUS: Welcome to the construct")
        print(f"Current Python: {sys.executable}")
        print(f"Virtual Environment: {venv_name}")
        print(f"Environment Path: {venv_path}")
        print("\nSUCCESS: You're in an isolated environment!")
        print("Safe to install packages without affecting")
        print("the global system.")
        print("\nPackage installation path:")
        print(package_path)


if __name__ == "__main__":
    main()
