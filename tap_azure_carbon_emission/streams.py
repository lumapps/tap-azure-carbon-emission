
from importlib import resources

from .client import AzureCarbonStream


SCHEMAS_DIR = resources.files(__package__) / "schemas"

class CarbonEmissionReportStream(AzureCarbonStream):
    name = "carbon_emission_reports"
    path = "/providers/Microsoft.Carbon/carbonEmissionReports?api-version=2025-04-01"
    primary_keys = ["dataType", "itemName"]  # Use actual fields that exist in records
    replication_key = "date"  # Use date field that exists in the response
    rest_method = "POST"
    schema_filepath = SCHEMAS_DIR / "carbon_emission_report.json"

