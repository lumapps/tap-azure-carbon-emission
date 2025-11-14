from singer_sdk import Tap
from .streams import CarbonEmissionReportStream

class TapAzureCarbonEmission(Tap):
    name = "tap-azure-carbon"
    config_jsonschema = {
        "type": "object",
        "properties": {
            "subscriptionList": {"type": "array", "items": {"type": "string"}},
            "carbonScopeList": {"type": "array", "items": {"type": "string"}},
            "start_date": {"type": "string", "format": "date"},
            "end_date": {"type": "string", "format": "date"},
            "reportType": {"type": "string"},
            "categoryType": {"type": "string"},
            "orderBy": {"type": "string"},
            "sortDirection": {"type": "string"},
            "pageSize": {"type": "integer"},
        },
        "required": ["reportType", "subscriptionList", "carbonScopeList", "start_date", "end_date"]
    }

    def discover_streams(self):
        return [CarbonEmissionReportStream(self)]

if __name__ == "__main__":
    TapAzureCarbonEmission.cli()
