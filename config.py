try:
    import config_local
except ImportError:
    print('Определите значение токена яндекс и рабочей директории ')

TOKEN_YANDEX = config_local.TOKEN_YANDEX

WORK_DIRECTORY = config_local.WORK_DIRECTORY

IMAGE_FORMATS = ['jpg', 'png']
ARCHIVE_FORMATS = ['zip', 'rar']
DOC_FILE_FORMATS = ['txt', 'docx', 'xlsx', 'csv', 'xls', 'pptx']
VIDEO_FORMATS = ['mp4', 'webm']