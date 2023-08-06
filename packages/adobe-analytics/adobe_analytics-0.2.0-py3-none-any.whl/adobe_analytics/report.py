import pandas as pd
import numpy as np
import more_itertools


class Report:
    def __init__(self, report_id):
        self.id = int(report_id)
        self.raw_response = None
        self.dataframe = None

    def parse(self):
        assert self.raw_response is not None, "Download report data first."
        raw_data = self.raw_response["report"]["data"]

        dimensions, metrics = self._parse_header()
        data = self._parse_data(raw_data, metric_count=len(metrics))
        header = self._fix_header(dimensions, metrics, data)

        self.dataframe = pd.DataFrame(data, columns=header)

    def _parse_header(self):
        report = self.raw_response["report"]

        dimensions = [self._classification_or_name(dimension) for dimension in report["elements"]]
        metrics = [metric["name"] for metric in report["metrics"]]
        return dimensions, metrics

    @staticmethod
    def _classification_or_name(element):
        if "classification" in element:
            return element["classification"]
        return element["name"]

    @staticmethod
    def _parse_data(data, metric_count):
        """
        Recursive parsing of the "data" part of the Adobe response.
        :param data: list of dicts and lists. quite a complicated structure
        :param metric_count: int, number of metrics in report
        :return: list of lists
        """
        if "breakdown" in data[0]:
            rows = list()
            for chunk in data:
                dim_is_none = "name" not in chunk or chunk["name"] == ""
                dim_value = np.nan if dim_is_none else chunk["name"]
                rows += [[dim_value] + row
                         for row in Report._parse_data(chunk["breakdown"], metric_count)]
            return rows
        else:
            return Report._parse_most_granular(data, metric_count)

    @staticmethod
    def _parse_most_granular(data, metric_count):
        """
        Parsing of the most granular part of the response.
        It is different depending on if there's a granularity breakdown or not
        :param data: dict
        :param metric_count: int, number of metrics in report
        :return: list of lists
        """
        rows = list()
        for chunk in data:
            dim_name = chunk["name"] if chunk["name"] != "" else np.nan
            # data alignment is a bit different if adding granularity breakdowns
            part_rows = [(val if val != "" else np.nan) for val in chunk["counts"]]
            if len(chunk["counts"]) > metric_count:
                part_rows = more_itertools.chunked(iterable=part_rows, n=metric_count+1)
            else:
                part_rows = [part_rows]
            rows += [[dim_name]+part_row for part_row in part_rows]
        return rows

    @staticmethod
    def _fix_header(dimensions, metrics, data):
        header = dimensions + metrics
        if len(header) != len(data[0]):  # can only be when granularity breakdown is used
            return ["Granularity"] + header
        return header


if __name__ == '__main__':
    print(type(response))

    report = Report(123)
    report.raw_response = response
    report.parse()
    print(report.dataframe)
