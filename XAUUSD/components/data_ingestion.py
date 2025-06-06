import os
import sys
import pandas as pd
from XAUUSD.exception.exception import XAUUSDException
from XAUUSD.logging.logger import logging
from XAUUSD.entity.config_entity import DataIngestionConfig
from XAUUSD.entity.artifact_entity import DataIngestionArtifact

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise XAUUSDException(e, sys)

    def load_data_from_csv(self) -> pd.DataFrame:
        try:
            raw_file_path = os.path.join("XAUUSD_Data", self.data_ingestion_config.raw_file_name)
            df = pd.read_csv(raw_file_path)
            df["Date"] = pd.to_datetime(df["Date"])  
            df = df.sort_values("Date")
            logging.info(f"Loaded data from {raw_file_path}")
            return df
        except Exception as e:
            raise XAUUSDException(e, sys)

    def export_data_to_feature_store(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            feature_store_path = self.data_ingestion_config.feature_store_file_path
            os.makedirs(os.path.dirname(feature_store_path), exist_ok=True)
            df.to_csv(feature_store_path, index=False)
            logging.info(f"Exported full dataset to feature store at {feature_store_path}")
            return df
        except Exception as e:
            raise XAUUSDException(e, sys)

    def split_and_save_train_test(self, df: pd.DataFrame):
        try:
            split_date = pd.to_datetime(self.data_ingestion_config.split_date)

            train_df = df[df["Date"] <= split_date]
            test_df = df[df["Date"] > split_date]

            os.makedirs(os.path.dirname(self.data_ingestion_config.training_file_path), exist_ok=True)

            train_df.to_csv(self.data_ingestion_config.training_file_path, index=False)
            test_df.to_csv(self.data_ingestion_config.testing_file_path, index=False)

            logging.info("Train/Test split successful.")
        except Exception as e:
            raise XAUUSDException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            df = self.load_data_from_csv()
            df = self.export_data_to_feature_store(df)
            self.split_and_save_train_test(df)

            return DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
        except Exception as e:
            raise XAUUSDException(e, sys)
