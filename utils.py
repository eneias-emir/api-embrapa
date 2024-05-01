import requests
import os
from AppConfig import AppConfig

def url_to_csv_filename(url: str) -> str:
    return AppConfig.PATH_DATA.value + url.rsplit("/", 1)[1]
def download_csv(url: str) -> None:
    file_name = url_to_csv_filename(url)

    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Save the content of the response to a local CSV file
        with open(file_name, "wb") as f:
            f.write(response.content)
        print("CSV file downloaded successfully")
    else:
        print("Failed to download CSV file. Status code:", response.status_code)

def database_file_exists() -> bool:
    db_file_name = AppConfig.DATABASE_NAME.value + AppConfig.DATABASE_EXTENSION.value
    working_dir = AppConfig.PATH_DATA.value
    db_file = os.path.join(working_dir, db_file_name)
    if not os.path.exists(db_file):
        return False
    else:
        return True


