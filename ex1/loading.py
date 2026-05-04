# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  loading.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: asulon <asulon@student.42nice.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/04 22:14:12 by asulon          #+#    #+#               #
#  Updated: 2026/05/04 22:15:37 by asulon          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import importlib
import sys
from typing import Any


REQUIRED_PACKAGES = ["pandas", "numpy", "matplotlib"]


def check_dependencies() -> tuple[dict[str, Any], list[str]]:
    print("LOADING STATUS: Loading programs...")
    print("Checking dependencies:")

    installed = {}
    missing = []

    for pkg in REQUIRED_PACKAGES:
        try:
            module = importlib.import_module(pkg)
            version = getattr(module, "__version__", "unknown")
            print(f"[OK] {pkg} ({version}) - ready")
            installed[pkg] = module
        except ImportError:
            print(f"[MISSING] {pkg} - not installed")
            missing.append(pkg)

    return installed, missing


def show_install_instructions(missing: list[str]) -> None:
    print("\nMissing dependencies detected!\n")

    print("Install with pip:")
    print("pip install " + " ".join(missing))

    print("\nOr using requirements.txt:")
    print("pip install -r requirements.txt")

    print("\nOr with Poetry:")
    print("poetry add " + " ".join(missing))

    print("\nThen run:")
    print("python loading.py")


def generate_data(np: Any) -> Any:
    print("\nAnalyzing Matrix data...")

    data = np.random.normal(loc=50, scale=15, size=1000)
    return data


def analyze_data(pd: Any, np: Any, data: Any) -> Any:
    print(f"Processing {len(data)} data points...")
    return pd.DataFrame({"signal_strength": data})


def visualize(matplotlib: Any, df: Any) -> None:
    print("Generating visualization...")

    plt = matplotlib.pyplot

    plt.figure()
    df["signal_strength"].hist(bins=50)
    plt.title("Matrix Signal Distribution")
    plt.xlabel("Signal Strength")
    plt.ylabel("Frequency")

    plt.savefig("matrix_analysis.png")


def main() -> None:
    installed, missing = check_dependencies()

    if missing:
        show_install_instructions(missing)
        sys.exit(1)

    pd = installed["pandas"]
    np = installed["numpy"]
    matplotlib = installed["matplotlib"]

    import matplotlib.pyplot

    data = generate_data(np)
    df = analyze_data(pd, np, data)

    visualize(matplotlib, df)

    print("\nAnalysis complete!")
    print("Results saved to: matrix_analysis.png")


if __name__ == "__main__":
    main()
