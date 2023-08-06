import time
import itertools

from adobe_analytics.report import Report
from adobe_analytics.report_definition import ReportDefinition


class ReportDownloader:
    def __init__(self, suite):
        self.suite = suite

    def download(self, obj):
        report = self._to_report(obj)
        print("ReportID:", report.id)  # TODO: should be logging

        report.raw_response = self.check_until_ready(report)
        report.parse()
        return report

    def _to_report(self, obj):
        assert isinstance(obj, (Report, ReportDefinition, dict, int, float))

        if isinstance(obj, Report):
            return obj
        elif isinstance(obj, (ReportDefinition, dict)):
            report_definition = ReportDefinition.assert_dict(obj)
            return self.queue(report_definition)
        else:
            return Report(report_id=obj)

    def queue(self, report_definition):
        client = self.suite.client

        report_definition = ReportDefinition.inject_suite_id(report_definition, self.suite.id)
        request_data = self._build_request_data_definition(report_definition)
        response = client.request(
            api="Report",
            method="Queue",
            data=request_data
        )
        report_id = response["reportID"]
        return Report(report_id)

    def check_until_ready(self, report):
        for poll_attempt in itertools.count():
            response = self.check(report)
            if response is not None:
                return response

            self._sleep(poll_attempt)

    @staticmethod
    def _sleep(poll_attempt):
        exponential = 5 * 2**poll_attempt
        interval = min(exponential, 300)  # max 5 min sleep
        time.sleep(interval)

    def check(self, report):
        client = self.suite.client

        request_data = self._build_request_data_id(report)
        response = client.request(
            api="Report",
            method="Get",
            data=request_data
        )
        is_ready = ("error" not in response) or (response["error"] != "report_not_ready")
        if is_ready:
            return response
        return None

    def cancel(self, report):
        client = self.suite.client

        request_data = self._build_request_data_id(report)
        response = client.request(
            api='Report',
            method='Cancel',
            data=request_data
        )
        return response

    @staticmethod
    def _build_request_data_definition(report_definition):
        report_definition = ReportDefinition.assert_dict(report_definition)
        assert report_definition["reportSuiteID"] is not None
        return {"reportDescription": report_definition}

    @staticmethod
    def _build_request_data_id(report):
        return {"reportID": report.id}
