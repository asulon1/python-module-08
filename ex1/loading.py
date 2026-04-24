"""Loading Programs exercise.

This script demonstrates dependency checks, simple data analysis,
and a pip vs Poetry comparison output.
"""

import importlib
import importlib.util
import sys
from importlib import metadata


CORE_PACKAGES = {
    "pandas": "Data manipulation ready",
    "numpy": "Numerical computation ready",
    "matplotlib": "Visualization ready",
}

OPTIONAL_PACKAGES = {
    "requests": "Network access ready",
}


def package_version(package_name: str) -> str:
    """Return installed package version or 'unknown'."""
    try:
        return metadata.version(package_name)
    except metadata.PackageNotFoundError:
        return "unknown"


def is_installed(package_name: str) -> bool:
    """Check whether a package is importable in current environment."""
    return importlib.util.find_spec(package_name) is not None


def print_dependency_comparison() -> None:
    """Show conceptual and runtime differences between pip and Poetry."""
    print("\nDependency management comparison:")
    print("- pip: installs from requirements.txt (direct package list)")
    print("- Poetry: installs from pyproject.toml (managed dependency graph)")
    print("- Poetry commonly uses an isolated virtual environment per project")

    is_venv = getattr(sys, "base_prefix", sys.prefix) != sys.prefix
    if is_venv:
        print("- Current runtime: virtual environment detected")
    else:
        print("- Current runtime: no virtual environment detected")
    print(f"- Python executable: {sys.executable}")

    print("\nInstalled package versions:")
    for package in [*CORE_PACKAGES.keys(), *OPTIONAL_PACKAGES.keys()]:
        if is_installed(package):
            print(f"  {package}: {package_version(package)}")


def check_dependencies():
    """Validate dependencies and import required modules if available."""
    print("Checking dependencies:")

    missing_core: list[str] = []
    for package, message in CORE_PACKAGES.items():
        if is_installed(package):
            print(f"[OK] {package} ({package_version(package)}) - {message}")
        else:
            print(f"[MISSING] {package} - required")
            missing_core.append(package)

    for package, message in OPTIONAL_PACKAGES.items():
        if is_installed(package):
            print(f"[OK] {package} ({package_version(package)}) - {message}")
        else:
            print(
                f"[INFO] {package} - optional (only needed for API fetching)")

    if missing_core:
        print("\nMissing required dependencies detected.")
        print("Install with pip:")
        print("  pip install -r requirements.txt")
        print("Install with Poetry:")
        print("  poetry install")
        print_dependency_comparison()
        return None

    modules = {
        "numpy": importlib.import_module("numpy"),
        "pandas": importlib.import_module("pandas"),
        "plt": importlib.import_module("matplotlib.pyplot"),
    }
    return modules


def build_matrix_dataset(np, pd, size: int = 1000):
    """Create synthetic Matrix-like data with NumPy as primary source."""
    ticks = np.arange(size)
    signal = np.sin(ticks / 27.0) + 0.25 * np.cos(ticks / 9.0)
    noise = np.random.normal(loc=0.0, scale=0.35, size=size)
    combined = signal + noise
    energy = np.square(combined)

    return pd.DataFrame(
        {
            "tick": ticks,
            "signal": combined,
            "energy": energy,
            "state": np.where(combined > 0.8, "awake", "sleeping"),
        }
    )


def analyze_and_plot(
    df,
    pd,
    plt,
    output_file: str = "matrix_analysis.png",
) -> None:
    """Run simple analysis and generate a plot image."""
    print("Analyzing Matrix data...")
    print(f"Processing {len(df)} data points...")

    rolling_window = 30
    df["rolling_signal"] = df["signal"].rolling(
        window=rolling_window, min_periods=1).mean()

    state_counts = df["state"].value_counts()
    summary = pd.DataFrame(
        {
            "mean_signal": [df["signal"].mean()],
            "max_energy": [df["energy"].max()],
            "awake_count": [int(state_counts.get("awake", 0))],
            "sleeping_count": [int(state_counts.get("sleeping", 0))],
        }
    )

    print("Summary:")
    print(summary.to_string(index=False))

    print("Generating visualization...")
    plt.figure(figsize=(10, 5))
    plt.plot(df["tick"], df["signal"], alpha=0.35, label="Signal")
    plt.plot(df["tick"], df["rolling_signal"],
             linewidth=2, label="Rolling mean")
    plt.title("Matrix Signal Analysis")
    plt.xlabel("Tick")
    plt.ylabel("Signal strength")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()

    print("Analysis complete!")
    print(f"Results saved to: {output_file}")


def main() -> int:
    """Program entrypoint."""
    print("LOADING STATUS: Loading programs...")
    modules = check_dependencies()
    if modules is None:
        return 1

    np = modules["numpy"]
    pd = modules["pandas"]
    plt = modules["plt"]

    # Seed for deterministic output between runs.
    np.random.seed(42)

    df = build_matrix_dataset(np, pd, size=1000)
    analyze_and_plot(df, pd, plt)
    print_dependency_comparison()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
