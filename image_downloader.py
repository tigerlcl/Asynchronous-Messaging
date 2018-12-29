# a program that is responsible for downloading images
# from either Telegram or a given URL
# Auther: Tiger Li
import json
import base64
import telepot
from PIL import Image
from io import BytesIO
from urllib import request
from redis import StrictRedis

r = StrictRedis(host='localhost', port=6379)
bot = telepot.Bot("YOUR BOT's TOKEN")

# define a simple function to process 'image.png'
def image_digit(image):
    image = Image.open(image)
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    encoded_image = base64.b64encode(buffered.getvalue())
    return encoded_image.decode('utf-8')

while True:
    print('listening to the message queue: download')
    _ , data = r.blpop('download') # _ stands for key: 'download'
    data = data.decode('utf-8')
    chat_id = json.loads(data)['chat_id']
    image_file = json.loads(data)['image']
    # file_id or URL
    print('download image...')
    if image_file.startswith('http'):
        request.urlretrieve(image_file, 'image.png')
    else:
        bot.download_file(image_file,'image.png')

    data = {'chat_id': chat_id, 'image': image_digit('image.png')}
    r.rpush('image', json.dumps(data).encode("utf-8"))
    print('downloaded and sent to queue: image')
