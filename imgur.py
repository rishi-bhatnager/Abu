# Testing imgur api
import configparser
from imgurpython import ImgurClient

config = configparser.ConfigParser()
config.read('auth.ini')

client_id = config.get('credentials', 'client_id')
client_secret = config.get('credentials', 'client_secret')

client = ImgurClient(client_id, client_secret)


def upload_image(file):
    img_dict = client.upload_from_path(file, config=None, anon=True)
    return img_dict['link']

def upload_all():
    arr = ['byAssetType.png', 'byIndustry.png', 'bySector.png', 'general.png']
    holder = []
    for a in arr:
        holder.append(upload_image(a))
    return holder

