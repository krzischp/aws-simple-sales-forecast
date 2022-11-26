import urllib.parse
import boto3
import pandas as pd
import requests
from datetime import datetime


def get_file_name(base_name):
    return datetime.now().strftime(f"%Y%m%d%H%M%S-{base_name}")


def create_structured_file(df):
    file_name = get_file_name('sample-urls.csv')
    local_csv_file = f'/tmp/{file_name}'

    i = 0

    for url in df.url:
        try:
            response = requests.get(url)
            response.raise_for_status()
            # access JSOn content
            jsonResponse = response.json()
            df.loc[i, "id"] = jsonResponse["id"]
            df.loc[i, "name"] = jsonResponse["name"]
            df.loc[i, "past_types"] = len(jsonResponse["past_types"])
            df.loc[i, "height"] = jsonResponse["height"]
            df.loc[i, "weight"] = jsonResponse["weight"]
            df.loc[i, "moves"] = len(jsonResponse["moves"])
            i += 1
    #         print(df.head())

        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')

    # SAVING TO CSV IN LOCAL FOLDER
    df.to_csv(local_csv_file, index=False)
    bucket_name = 'simple-forecast-structured-files-bucket'

    s3 = boto3.resource("s3")
    s3.meta.client.upload_file(local_csv_file, bucket_name, file_name)


def lambda_handler(event, context):
    s3_client = boto3.resource('s3')
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        object = s3_client.Object(bucket, key)
        # file_content = object.get()['Body'].read()
        urls = pd.read_csv(object.get()['Body'], names=["url"])
        # create_structured_file(file_content)
        create_structured_file(urls)
        return 'SUCCESS'
    except Exception as e:
        print(e)
        print(f'Error getting object {key} from bucket {bucket}.')
        raise e
