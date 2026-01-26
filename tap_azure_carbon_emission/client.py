from enum import Enum
from typing import Any, Optional
import json

import requests
from singer_sdk.streams import RESTStream
from singer_sdk.authenticators import BearerTokenAuthenticator

class AzureCarbonStream(RESTStream):

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config.get("base_url", "https://management.azure.com/")

    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        return BearerTokenAuthenticator(self, token=self.config["access_token"])

    def prepare_request_payload(
        self,
        context: Optional[dict],
        next_page_token: Optional[Any] = None,
    ) -> Optional[dict]:
        """Prepare the data payload for the REST API request."""
        report_type = self.config["report_type"]

        payload = {
            "reportType": report_type,
            "subscriptionList": self.config["subscription_list"],
            "carbonScopeList": self.config["carbon_scope_list"],
            "dateRange": {
                "start": self.config["start_date"],
                "end": self.config["end_date"]
            },
        }

        # Extra fields by report type
        extra_fields = {
            "ItemDetailsReport": {
                "categoryType": self.config.get("category_type"),
                "orderBy": self.config.get("order_by"),
                "pageSize": self.config.get("page_size", 100),
                "sortDirection": self.config.get("sort_direction"),
            },
            "TopItemsSummaryReport": {
                "categoryType": self.config.get("category_type"),
                "topItems": self.config.get("top_items"),
            },
            "TopItemsMonthlySummaryReport": {
                "categoryType": self.config.get("category_type"),
                "topItems": self.config.get("top_items"),
            },
        }

        if report_type in extra_fields:
            payload.update({k: v for k, v in extra_fields[report_type].items() if v is not None})

        # Optional filters
        for field in ["location_list", "resource_group_url_list", "resource_type_list"]:
            if field in self.config:
                payload[field] = self.config[field]

        # Pagination
        if next_page_token:
            payload["skipToken"] = next_page_token

        # Log the payload for debugging
        self.logger.info(f"API Request Payload: {json.dumps(payload, indent=2)}")

        return payload

    def get_next_page_token(self, response, previous_token) -> Optional[Any]:
        resp_json = response.json()
        return resp_json.get("skipToken")

    def parse_response(self, response):
        data = response.json()
        return data.get("value", [])
