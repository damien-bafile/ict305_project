import requests

def download_dataset(file):
    """
    :param file: The file path where the downloaded dataset will be saved.
    :return: None
    """
    url = "https://www.wa.gov.au/media/48429/download?inline?inline="
    response = requests.get(url)
    with open(file, "wb") as f:
        f.write(response.content)