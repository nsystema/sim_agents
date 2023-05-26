import os
import re
from tqdm import tqdm
from google.cloud import storage



def download_from_gcs(gcs_path):
    # Extract the filename from the file URL
    filename = re.search('/(training|testing|validation)/(.+\.tfrecord-\d+-of-\d+)', gcs_path).group(2)
    # if waymo open dataset folder does not exist, create it
    if not os.path.exists('waymo_open_dataset_'):
        os.makedirs('waymo_open_dataset_')
    # local path
    local_path = 'waymo_open_dataset_/' + filename
    # check if the file already exists 
    if os.path.isfile(local_path):
        print(f'{filename} already exists in {local_path}')
    else:
        # Set up the storage client with api key: AIzaSyAtD_clSdxcEp4YXa2gWtFuhi6xSEEb_K8
        client = storage.Client.from_service_account_json('waymo-od-1-2-0-fb3a3a0b6e6e.json')
        # Get a reference to the bucket and object
        bucket = client.bucket('waymo_open_dataset_motion_v_1_2_0')
        blob = bucket.blob(gcs_path)

        # Download the object to a file with a progress bar
        with tqdm.wrapattr(open(local_path, 'wb'), 'write', miniters=1,
                          total=blob.size, desc=f'Downloading {gcs_path}') as file_obj:
            blob.download_to_file(file_obj)

        print(f'Object downloaded to {local_path}')