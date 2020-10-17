# Testing imgur api
import configparser
from imgurpython import ImgurClient

config = configparser.ConfigParser()
config.read('auth.ini')

client_id = config.get('credentials', 'client_id')
client_secret = config.get('credentials', 'client_secret')

client = ImgurClient(client_id, client_secret)
# img_dict = client.upload_from_path('foo.png', config=None, anon=True)
# print(img_dict['link'])
print(client.credits)
