from singer_sdk import Tap
from .streams import CarbonEmissionReportStream
from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Dict, Any

class TapAzureCarbonEmission(Tap):
    name = "tap-azure-carbon"
    config_jsonschema = {
        "type": "object",
        "properties": {
            "subscription_list": {"type": "array", "items": {"type": "string"}},
            "carbon_scope_list": {"type": "array", "items": {"type": "string"}},
            "start_date": {
                "type": "string", 
                "format": "date",
                "description": "Start date (ISO 8601). If not provided, automatically uses last month to handle API delay."
            },
            "end_date": {
                "type": "string", 
                "format": "date",
                "description": "End date (ISO 8601). If not provided, automatically uses last month to handle API delay."
            },
            "report_type": {"type": "string"},
            "category_type": {"type": "string"},
            "order_by": {"type": "string"},
            "sort_direction": {"type": "string"},
            "page_size": {"type": "integer"},
        },
        "required": ["report_type", "subscription_list", "carbon_scope_list"]
    }

    # Report types that require same start and end date (single month only)
    SINGLE_MONTH_REPORTS = ["ItemDetailsReport", "TopItemsSummaryReport"]
    
    def __init__(self, config: Dict[str, Any] = None, *args, **kwargs):
        # Calculate dates before passing config to parent
        if config:
            config = self._calculate_dynamic_dates(config)
        super().__init__(config=config, *args, **kwargs)

    def _calculate_dynamic_dates(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate start_date and end_date automatically for last month if not provided."""
        report_type = config.get("report_type")
        
        # If dates are not provided, automatically use last month (to handle API delay)
        if "start_date" not in config or "end_date" not in config:
            today = datetime.now()
            
            # Calculate last month (first day)
            last_month = today - relativedelta(months=1)
            start_date = last_month.replace(day=1)
            
            # Determine end date based on report type constraints
            if report_type in self.SINGLE_MONTH_REPORTS:
                # Single-month reports: start and end must be the same (first day of month)
                end_date = start_date
                self.logger.info(
                    f"Auto-calculated dates for '{report_type}': start_date=end_date={start_date.strftime('%Y-%m-%d')} "
                    f"(last month to handle API delay)"
                )
            else:
                # Date range reports: use full last month
                next_month = start_date + relativedelta(months=1)
                end_date = next_month - relativedelta(days=1)
                
                self.logger.info(
                    f"Auto-calculated dates for '{report_type}': start_date={start_date.strftime('%Y-%m-%d')}, "
                    f"end_date={end_date.strftime('%Y-%m-%d')} (last month to handle API delay)"
                )
            
            # Set the calculated dates in config
            config["start_date"] = start_date.strftime("%Y-%m-%d")
            config["end_date"] = end_date.strftime("%Y-%m-%d")
            
        else:
            # Manual dates provided - validate based on report type
            if report_type in self.SINGLE_MONTH_REPORTS:
                if config["start_date"] != config["end_date"]:
                    self.logger.info(
                        f"Report type '{report_type}' requires start_date to equal end_date. "
                        f"Using start_date={config['start_date']} for both."
                    )
                    config["end_date"] = config["start_date"]
        
        return config

    def discover_streams(self):
        return [CarbonEmissionReportStream(self)]

if __name__ == "__main__":
    TapAzureCarbonEmission.cli()
