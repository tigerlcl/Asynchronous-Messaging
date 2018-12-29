# keep receiving user messages from Telegram
# Be responsible for sending response back to the user
# Auther: Tiger Li

import time
import telepot
import base64
import json
from redis import StrictRedis
from threading import Thread
from telepot.loop import MessageLoop

r = StrictRedis(host='localhost', port=6379)

def handle(msg):
    """
    A thread that process message from user
    submit to queue: download
    """
    content_type, chat_type, chat_id = telepot.glance(msg)
    image_file = None
    # received URL for image
    if content_type == "text":
        content = msg["text"]
        if not content.startswith("http"):
            print('invalid URL, waiting for another input')
        else:
            print('received URL, submit it to queue: download')
            image_file = content
    # received photos from user
    elif content_type == 'photo':
        print('received image, submit file_id to queue: download!')
        image_file = msg['photo'][-1]['file_id']
        # args = -1 keeps the original size of image
    else:
        print('can\'t recognize, waiting for another input')

    if image_file:
        data = {'chat_id': chat_id, 'image': image_file}
        r.rpush('download', json.dumps(data).encode("utf-8"))

def response_thread():
    """
    A thread that takes results from the client thread,
    then format a message and send it back to the user.
    """
    while True:
        print('listening to the message queue: prediction')
        _ , data = r.blpop('prediction') # _ stands for key: 'download'
        data = data.decode('utf-8')
        chat_id = json.loads(data)['chat_id']
        reply = json.loads(data)['predictions']

        messages = '' # store entire message to sent to user
        for item in reply:
            messages += '{} ({})\n'.format(item['label'], item['score'])
        bot.sendMessage(chat_id, messages)
        print('pridictions sent to user{}!'.format(chat_id))

if  __name__ == "__main__":
    print('Initializing the bot...')

    # Start the thread
    Thread(target=response_thread).start()
    print("Thread 1&2 started")
    # Provide your bot's token e.g., 12345678:A1B2C3D4E5-6F7G
    bot = telepot.Bot("YOUR BOT's TOKEN")
    MessageLoop(bot, handle).run_as_thread()

    while True:
        time.sleep(5)
