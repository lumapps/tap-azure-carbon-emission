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

### Required Settings

- `access_token`: Azure Bearer token for authentication
- `subscription_list`: Array of Azure subscription IDs
- `carbon_scope_list`: Array of carbon scope types (default: ["Scope1", "Scope3"])
- `report_type`: Type of report to generate (default: MonthlySummaryReport)

### Date Configuration

#### Automatic (Recommended)

- Simply omit `start_date` and `end_date` - the tap automatically fetches data from last month to handle the Azure API's one-month delay
- For single-month reports (ItemDetailsReport, TopItemsSummaryReport): Sets both dates to the first day of last month
- For range reports: Fetches the full last month

##### Manual Dates (Optional)

- `start_date`: Start date for the report (ISO 8601 format)
- `end_date`: End date for the report (ISO 8601 format)
- When provided, these override the automatic date calculation

### Report Types and Date Constraints

| Report Type                    | Date Constraint               | Description                                            |
| ------------------------------ | ----------------------------- | ------------------------------------------------------ |
| `OverallSummaryReport`         | Date range allowed            | Total emissions for date range with comparative values |
| `MonthlySummaryReport`         | Date range allowed            | Monthly emissions data for specified range             |
| `TopItemsSummaryReport`        | Single month only (start=end) | Top N emitters for one month                           |
| `TopItemsMonthlySummaryReport` | Date range allowed            | Top N emitters by month                                |
| `ItemDetailsReport`            | Single month only (start=end) | Granular item list for one month                       |

See [Azure website](https://learn.microsoft.com/en-us/azure/carbon-optimization/api-export-data?source=recommendations&tabs=OverallSummaryReport#report-types) for details.

### Additional Settings

- `category_type`: Category for ItemDetailsReport (Resource, ResourceGroup, Service)
- `order_by`: Sort field for ItemDetailsReport
- `sort_direction`: Sort direction (Asc, Desc)
- `page_size`: Items per page for ItemDetailsReport

## Usage Examples

### Example 1: ItemDetailsReport with Automatic Dates (Recommended)

```json
{
  "access_token": "your_token",
  "subscription_list": ["subscription-id"],
  "carbon_scope_list": ["Scope1", "Scope2", "Scope3"],
  "report_type": "ItemDetailsReport",
  "category_type": "Resource",
  "page_size": 2000
}
```

This automatically fetches data from last month.

### Example 2: MonthlySummaryReport with Manual Dates

```json
{
  "access_token": "your_token",
  "subscription_list": ["subscription-id"],
  "carbon_scope_list": ["Scope1", "Scope2", "Scope3"],
  "report_type": "MonthlySummaryReport",
  "start_date": "2025-10-01",
  "end_date": "2025-12-31"
}
```

This fetches a specific date range (October to December 2025).

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
