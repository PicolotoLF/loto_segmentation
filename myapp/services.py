import datetime as dt

import numpy as np
import pandas as pd

from django.conf import settings
from google_spreadsheets.credentials import get_sheet


def get_values_from_spreadsheet(client_secret_json, url, sheet_name):
    # cs_json = json.loads(client_secret_json.read().decode('utf8'))
    sheet = get_sheet(settings.PROJECT_ROOT+client_secret_json.name, url, sheet_name)
    values = sheet.get_all_records()
    return values


class RFMCalculator:
    def __init__(self, values, score_boundary_frequency, score_boundary_monetary):
        self.values = values
        self._df = None
        self._df_date = None
        self._df_merged = None
        self._df_score_frequency = None
        self._df_score_monetary = None
        self._score_boundary_frequency = score_boundary_frequency
        self._score_boundary_monetary = score_boundary_monetary
        self._boundary_frequency = None
        self._boundary_monetary = None

    def _create_dataframe(self):
        self._df = pd.DataFrame(list(self.values))
        self._df["order_date_min"] = self._df["order_date"]
        self._df["avg_monetary"] = self._df["order_value"]
        self._df["frequency"] = self._df["customer_id"]

        self._df_date = self._df[["customer_id", "order_date"]]

    def _agregate_values_by_id(self):
        self._df = (self._df.groupby("customer_id").agg({"order_value": "sum",
                                             "order_date": "max",
                                             "order_date_min": "min",
                                             "avg_monetary": "mean",
                                             "frequency": "count"})
                    .reset_index()
                    .rename(columns={'order_value': 'monetary'}))

    def _add_recency(self):
        self._df["today"] = dt.date.today()
        self._df["recency"] = pd.to_datetime(self._df["order_date"]) - pd.to_datetime(self._df["today"])
        self._df["first_purchase"] = pd.to_datetime(self._df["order_date_min"]) - pd.to_datetime(self._df["today"])

        self._df["recency"] = self._df.apply(lambda x: x["recency"].days, axis=1)
        self._df["first_purchase"] = self._df.apply(lambda x: x["first_purchase"].days, axis=1)

    def _create_dates_values(self):
        self._df_date["order_date"] = pd.to_datetime(self._df_date["order_date"])

        new_df = pd.DataFrame({"customer_id": [],
                               "diff_date": []})
        for customer_id in self._df_date.groupby("customer_id")["customer_id"]:
            filter_values = \
                self._df_date[self._df_date["customer_id"] == customer_id[0]].sort_values(["customer_id", "order_date"])[
                "order_date"].diff(periods=-1)
            temp_df = pd.DataFrame({"customer_id": customer_id[0],
                                    "diff_date": filter_values})
            new_df = new_df.append(temp_df)

        new_df["diff_date"] = new_df.apply(lambda x: x["diff_date"].days, axis=1)
        new_df["customer_id"] = new_df["customer_id"].astype(int)
        new_df["std_dev"] = new_df["diff_date"]

        self._df_date = new_df.groupby("customer_id").agg({"diff_date": "mean",
                                                    "std_dev": np.std})

    def _merge_dfs(self, df1, df2, key):
        df_merged = pd.merge(df1, df2, on=[key, key])
        return df_merged

    def _create_score_tables(self):
        self._df_score_frequency = self._df_merged[["customer_id", "frequency", ]]
        self._df_score_monetary = self._df_merged[["customer_id", "monetary", ]]

    @staticmethod
    def _score(value):
        if value < .2:
            return 1
        elif value < .4:
            return 2
        elif value < .6:
            return 3
        elif value < .8:
            return 4
        else:
            return 5

    def _calculate_score(self, df_score, name):

        df_score_edited = df_score.sort_values(name, ascending=False).rolling(min_periods=1,
                                                                                 window=df_score[name].count(),
                                                                                 on="customer_id").sum()

        df_score_edited["customer_id"] = df_score_edited["customer_id"].astype(int)

        last_value = df_score_edited[name].iloc[-1]
        df_score_edited["per_{}".format(name)] = df_score_edited[name].apply(lambda x: (x / last_value))

        df_score_edited["score_{}".format(name)] = df_score_edited["per_{}".format(name)].apply(lambda x: self._score(x))

        return df_score_edited[["customer_id", "score_{}".format(name)]]

    def calculate_values(self):
        self._create_dataframe()
        self._agregate_values_by_id()
        self._add_recency()
        self._create_dates_values()
        self._df_merged = self._merge_dfs(self._df, self._df_date, "customer_id")

        self._create_score_tables()
        frequency_score = self._calculate_score(self._df_score_frequency, "frequency")
        self._df_merged = self._merge_dfs(self._df_merged, frequency_score, "customer_id")

        monetary_score = self._calculate_score(self._df_score_monetary, "monetary")
        self._df_merged = self._merge_dfs(self._df_merged, monetary_score, "customer_id")

        self._boundary_frequency = self._create_boundaries(self._df_merged, "score_frequency",
                                                           self._score_boundary_frequency,
                                                          "frequency")
        self._boundary_monetary = self._create_boundaries(self._df_merged, "score_monetary",
                                                          self._score_boundary_monetary,
                                                         "monetary")
        self._df_merged.fillna(0, inplace=True)
        return self._df_merged

    def to_dict(self):
        return self._df_merged.to_dict("records")

    @staticmethod
    def _create_boundaries(df, score_name, score_value, value_name):
        return df[df[score_name] == score_value][value_name].mean()

    @property
    def boundary_monetary(self):
        return self._boundary_monetary

    @property
    def boundary_frequency(self):
        return self._boundary_frequency




            # def create_matrix():
    #     # create matrix of between frequency and monetary
    #     pass
    #
    # def name_segments():
    #     # give segment name for each customer
    #     pass