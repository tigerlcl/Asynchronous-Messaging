# Asynchronous Messaging
### Description
In this project, I created an application that performs object recognition using a deep learning model. However, I will make some changes to the system by replacing direct TCP connections with asychronous messaging using Redis.
### Implementation
There are three components in this system:
1. bot.py: a program that keep receiving user messages from Telegram, and is also responsible for sending response back to the user
2. image_downloader.py: a program that is responsible for downloading images from either Telegram or a given URL
3. predict.py: a program that loads a PyTorch pre-trained model for object recognition, and generates predictions when given an image

model details: PyTorch pre-trained InceptionV3 model 

### Bonus: Load Balancing
Once you have finished all the scripts. You can experiment with starting multiple instance of image_downloader.py and predict.py. You should see that they will consume messages from the message queues alternatively, which the need to do any configurations on the scripts.
