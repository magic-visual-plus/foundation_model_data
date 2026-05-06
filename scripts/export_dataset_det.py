import os
import sys
import yaml
import sqlalchemy
from sqlalchemy import text
from minio import Minio
import json
from tqdm import tqdm
import loguru
import utils
import storage


logger = loguru.logger


bucket_name = "vision"
        

if __name__ == "__main__":
    data_config_file = sys.argv[1]
    output_path = sys.argv[2]

    connection = utils.get_sql_connection()
    client = storage.StorageCos()

    with open(data_config_file, 'r') as f:
        data_config = yaml.safe_load(f)
        pass

    for foundation_model_name, foundation_model_data in data_config['foundation_models'].items():
        fm_path = os.path.join(output_path, foundation_model_name)
        os.makedirs(fm_path, exist_ok=True)
        for project_name, project_data in foundation_model_data['projects'].items():
            project_path = os.path.join(fm_path, project_name)
            datasets = project_data.get('datasets', [])
            if len(datasets) == 0:
                approach_id = project_data.get('approach_id', None)
                if approach_id is None:
                    raise RuntimeError("Either datasets or approach_id must be specified in project")
                datasets = utils.get_datasets_from_approach(connection, approach_id)
                pass
            utils.export_datasets_det(connection, client, datasets, project_path)
            pass
        pass
    pass