import re
from my_exceptions import CloudCreateFolderError, DownloadDiskError, DownloadedFileError
import config
import requests
import os
from zipfile import ZipFile
import hashlib


class Data:

    type_data = {
                 "images": [],
                 "documents": [],
                 "videos": [],
                 "folder": []
                 }
    files_archived = []

    writed_files = []


class YandexDisk:
    def __init__(self):
        self.files_in_available_list_dict = []
        self.HEADERS = {"content-type": "application/json",
                        "charset": "utf-8",
                        "Authorization": f"OAuth {config.TOKEN_YANDEX}"}

    def create_folder_or_pass(self):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/'
        headers = self.HEADERS
        params = {"path": "auto_archive"}

        response = requests.put(url=url, headers=headers, params=params)


        if response.status_code == 409:
            pass

        elif response.status_code == 201:
            print('Создал папку на облаке')

        else:
            raise CloudCreateFolderError

    def get_list_files_from_disk(self):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/'
        headers = self.HEADERS
        params = {"path": "auto_archive"}

        response = requests.get(url=url, headers=headers, params=params)
        response = response.json()

        list_data_files = response['_embedded']['items']
        self.files_in_available_list_dict = list_data_files
        return list_data_files

    def download_from_disk(self, name_file: str, url_file: str):
        url = url_file
        response = requests.get(url, stream= True)

        os.chdir(config.WORK_DIRECTORY)

        with open(name_file, "wb") as handle:
            for data in response.iter_content():
                handle.write(data)

    def download_on_disk(self):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.HEADERS

        files_is_available_on_disk = []
        for file in self.files_in_available_list_dict:
            files_is_available_on_disk.append(file['name'])

        for archive in Data.files_archived:

            if archive in files_is_available_on_disk:
                print(f"Файл {archive} уже есть в облаке")

            else:
                params = {"path": f"disk:/auto_archive/{archive}", 'overwrite': 'true', 'fields': 'href'}
                response = requests.get(url=url, headers=headers, params=params)
                response = response.json()
                download_link = response.get('href')

                print(f"Загружаю файл ---> {archive}")
                data = open(f'{archive}', "rb")
                response = requests.put(url=download_link, headers=headers, params=params, data=data)

                print(F"STATUS DOWLOAD = {response.status_code}")

                if response.status_code != 201:
                    raise DownloadDiskError

                Data.writed_files.append(archive)


class Archivator:


    def create_archive(self, name_archive: str):

        # type is key, files is list
        for type, files in Data.type_data.items():

            if len(files) == 0:
                continue

            elif type == "folder":
                for folder in files:
                    with ZipFile(f"{folder}_{name_archive}.zip", 'w') as zipObj:
                        Data.writed_files.append(folder)
                        zipObj.write(f'{folder}')

            else:
                with ZipFile(f"{type}_{name_archive}.zip", 'w') as zipObj:

                    for file in files:
                        Data.writed_files.append(file)
                        zipObj.write(f'{file}')

    def add_file_in_archive(self, list_files: list):

        os.chdir(config.WORK_DIRECTORY)
        with ZipFile("image.zip", "a") as zipObj:
            for file in list_files:
                file_format = file.split('.')
                file_format = file_format[-1]
                print(file_format)

                if file_format in config.IMAGE_FORMATS:
                    zipObj.write(f'{file}')

    def extract_zip_file(self, file_name: str):
        work_dir = os.chdir(config.WORK_DIRECTORY)
        with ZipFile(f"{file_name}.zip", 'r') as zipObj:
            zipObj.extractall(work_dir)


class HashMd5:
    def check_downloaded_files(self):

        files_in_disk = YandexDisk().get_list_files_from_disk()

        for file_disk in files_in_disk:
            for file_pc in Data.files_archived:
                if file_disk["name"] == file_pc:

                    with open(f'{file_pc}', 'rb') as f:

                        hash = hashlib.md5()
                        hash.update(f.read())

                        hash_md_5 = hash.hexdigest()
                        if file_disk['md5'] != hash_md_5:
                            raise DownloadedFileError

                        else:
                            print(f'Проверил файл {file_pc}, md5 совпадает')


class MyPC:
    def __init__(self):
        self.files_in_directory = []

    def get_list_files_work_dir(self, PATH=None):
        if PATH is None:
            PATH = os.getcwd()

        files = os.listdir(PATH)
        self.files_in_directory = files

        for file in files:
            format_file = self.format_file(file)

            if format_file in config.IMAGE_FORMATS:
                Data.type_data["images"].append(file)

            elif format_file in config.DOC_FILE_FORMATS:
                Data.type_data["documents"].append(file)

            elif format_file in config.VIDEO_FORMATS:
                Data.type_data["videos"].append(file)

            elif format_file in config.ARCHIVE_FORMATS:
                Data.files_archived.append(file)

            elif self.is_folder(file) is True:
                Data.type_data["folder"].append(file)

        return files

    def format_file(self, file_name: str):
        file_format = file_name.split('.')
        file_format = file_format[-1]
        return file_format

    def delete_pedding_files(self, writed_files: list):

        for file in writed_files:
            try:
                os.remove(file)
            except:
                print(f" не смог удалить файл ---> {file}")

    def is_folder(self, file: str) -> bool:
        pattern = '[fF]older'
        result = re.search(pattern=pattern, string=file)


        if result is not None:
            return True






