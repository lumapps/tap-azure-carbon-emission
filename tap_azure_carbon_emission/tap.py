from singer_sdk import Tap
from .streams import CarbonEmissionReportStream

class TapAzureCarbonEmission(Tap):
    name = "tap-azure-carbon"
    config_jsonschema = {
        "type": "object",
        "properties": {
            "subscription_list": {"type": "array", "items": {"type": "string"}},
            "carbon_scope_list": {"type": "array", "items": {"type": "string"}},
            "start_date": {"type": "string", "format": "date"},
            "end_date": {"type": "string", "format": "date"},
            "report_type": {"type": "string"},
            "category_type": {"type": "string"},
            "order_by": {"type": "string"},
            "sort_direction": {"type": "string"},
            "page_size": {"type": "integer"},
        },
        "required": ["report_type", "subscription_list", "carbon_scope_list", "start_date", "end_date"]
    }

    def discover_streams(self):
        return [CarbonEmissionReportStream(self)]

if __name__ == "__main__":
    TapAzureCarbonEmission.cli()
