# Databricks notebook source
"""Download EPA AQS pre-generated data files into a Unity Catalog volume.

Source: https://aqs.epa.gov/aqsweb/airdata/download_files.html (public domain).

Run it as a Databricks notebook, or locally:
    python src/ingestion/download_aqs.py --dest ./data/aqs --years 2021 2025

Files land as unzipped CSVs, one folder per dataset:
    <dest>/daily_44201/daily_44201_2021.csv
    <dest>/aqs_sites/aqs_sites.csv
Auto Loader picks them up from there for the bronze layer.
"""

import argparse
import io
import os
import sys
import time
import urllib.request
import zipfile

BASE_URL = "https://aqs.epa.gov/aqsweb/airdata"

# Daily summary files, by parameter code
DAILY_PARAMETERS = {
    "44201": "ozone",
    "88101": "pm25_frm",
    "42602": "no2",
}

# Reference files that are not split by year
REFERENCE_FILES = ["aqs_sites", "aqs_monitors"]

DEFAULT_DEST = "/Volumes/aq/bronze/raw/aqs"
DEFAULT_FIRST_YEAR = 2021
DEFAULT_LAST_YEAR = 2025


def yearly_files(first_year, last_year):
    """Names of the per-year zip files to fetch, without extension."""
    names = []
    for year in range(first_year, last_year + 1):
        for code in DAILY_PARAMETERS:
            names.append(f"daily_{code}_{year}")
        names.append(f"daily_aqi_by_county_{year}")
    return names


def dataset_folder(name):
    """Folder for a file: daily_44201_2021 -> daily_44201, aqs_sites -> aqs_sites."""
    parts = name.rsplit("_", 1)
    if len(parts) == 2 and parts[1].isdigit():
        return parts[0]
    return name


def download_and_extract(name, dest, overwrite=False, retries=3):
    folder = os.path.join(dest, dataset_folder(name))
    target = os.path.join(folder, f"{name}.csv")
    if os.path.exists(target) and not overwrite:
        print(f"skip   {name} (already downloaded)")
        return target

    url = f"{BASE_URL}/{name}.zip"
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(url, timeout=120) as resp:
                payload = resp.read()
            break
        except Exception as exc:
            if attempt == retries:
                raise RuntimeError(f"failed to download {url}: {exc}") from exc
            wait = 2 ** attempt
            print(f"retry  {name} in {wait}s ({exc})")
            time.sleep(wait)

    os.makedirs(folder, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        csv_names = [n for n in archive.namelist() if n.lower().endswith(".csv")]
        if len(csv_names) != 1:
            raise RuntimeError(f"expected one CSV in {url}, found {csv_names}")
        with archive.open(csv_names[0]) as src, open(target, "wb") as out:
            out.write(src.read())

    print(f"saved  {name} ({len(payload) / 1_000_000:.1f} MB zipped)")
    return target


def run(dest, first_year, last_year, overwrite=False):
    names = REFERENCE_FILES + yearly_files(first_year, last_year)
    print(f"Downloading {len(names)} files to {dest}")
    for name in names:
        download_and_extract(name, dest, overwrite=overwrite)
    print("Done")


def in_databricks():
    return "DATABRICKS_RUNTIME_VERSION" in os.environ


# COMMAND ----------

if __name__ == "__main__" and not in_databricks():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dest", default="./data/aqs")
    parser.add_argument("--years", nargs=2, type=int, metavar=("FIRST", "LAST"),
                        default=[DEFAULT_FIRST_YEAR, DEFAULT_LAST_YEAR])
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    run(args.dest, args.years[0], args.years[1], overwrite=args.overwrite)
    sys.exit(0)

# COMMAND ----------

# In Databricks, set these as notebook widgets or job parameters
if in_databricks():
    dbutils.widgets.text("dest", DEFAULT_DEST)  # noqa: F821
    dbutils.widgets.text("first_year", str(DEFAULT_FIRST_YEAR))  # noqa: F821
    dbutils.widgets.text("last_year", str(DEFAULT_LAST_YEAR))  # noqa: F821
    run(
        dbutils.widgets.get("dest"),  # noqa: F821
        int(dbutils.widgets.get("first_year")),  # noqa: F821
        int(dbutils.widgets.get("last_year")),  # noqa: F821
    )
