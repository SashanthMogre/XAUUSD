from XAUUSD.components.data_ingestion import DataIngestion
from XAUUSD.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from XAUUSD.exception.exception import XAUUSDException
from XAUUSD.logging.logger import logging
from XAUUSD.entity.artifact_entity import DataIngestionArtifact
import sys

if __name__ == "__main__":
    try:
        logging.info("Pipeline started ✅")

        # 1. Create pipeline config
        training_pipeline_config = TrainingPipelineConfig()

        # 2. Create data ingestion config
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)

        # 3. Run data ingestion
        data_ingestion = DataIngestion(data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

        logging.info("Data Ingestion Completed ✅")
        print("Training File:", data_ingestion_artifact.trained_file_path)
        print("Testing File :", data_ingestion_artifact.test_file_path)

    except Exception as e:
        raise XAUUSDException(e, sys)
