import os
from datetime import datetime
import config
from tqdm import tqdm, trange
from yandex import YandexDisk, Archivator, MyPC, HashMd5, Data

if __name__=="__main__":
    YandexDisk = YandexDisk()
    Archivator = Archivator()
    MyPC = MyPC()
    HashMd5 = HashMd5()
    WORK_DIR = config.WORK_DIRECTORY

    # switch work directory
    os.chdir(WORK_DIR)

    # create folder in Yandex Disk if not exists, default = "auto_archive"
    YandexDisk.create_folder_or_pass()

    YandexDisk.get_list_files_from_disk()
    MyPC.get_list_files_work_dir()

    # if not files in work directory
    if MyPC.files_in_directory == []:
        print(" Нет файлов в директории ")

    # if files available in work directory
    else:
        # for name file archived using data and type data. For example: 00_34_16_08_Feb_2022_images.zip
        name_archive = datetime.now().strftime("%X_%d_%b_%Y").replace(':', '_')
        print(f'Наличие данных ---> {Data.type_data}')

        # all data archived
        Archivator.create_archive(name_archive=name_archive)

        # update work directory
        MyPC.get_list_files_work_dir()

        YandexDisk.download_on_disk()

        #check downloaded archive files and archived files in work directory with md5
        HashMd5.check_downloaded_files()

        MyPC.delete_pedding_files(Data.writed_files)

    input('press enter to continue')














