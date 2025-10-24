# tap-azure-carbon-emission

A Singer tap for extracting data from the Azure Carbon Emission API.

This tap extracts carbon emission data from Azure's sustainability reporting API, providing insights into carbon footprint for Azure subscriptions.

## Features

- Multiple report types: Monthly Summary, Item Details, Top Items Summary
- Configurable carbon scopes (Scope1, Scope3)
- Date range filtering
- Pagination support
- Authentication via Bearer tokens

## Installation

```bash
pip install -e .
```

## Configuration

Configure the tap with the following settings:

- `access_token`: Azure Bearer token for authentication
- `subscriptionList`: Array of Azure subscription IDs
- `carbonScopeList`: Array of carbon scope types (default: ["Scope1", "Scope3"])
- `start_date`: Start date for the report (ISO 8601 format)
- `end_date`: End date for the report (ISO 8601 format)
- `reportType`: Type of report to generate (default: MonthlySummaryReport)

## Usage with Meltano

```yaml
extractors:
- name: tap-azure-carbon-emission
  namespace: tap_azure_carbon_emission
  pip_url: -e .
  settings:
    access_token: your_azure_token
    subscriptionList: ["subscription-id"]
    start_date: "2024-01-01"
    end_date: "2024-12-31"
```
