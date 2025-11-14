"""TapAzureCarbon entry point."""

from __future__ import annotations

from tap_azure_carbon_emission.tap import TapAzureCarbon

TapAzureCarbon.cli()