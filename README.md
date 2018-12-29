

In this project, I created an application that performs object recognition using a deep learning model. However, I will make some changes to the system by replacing direct TCP connections with asychronous messaging using Redis.

There are three components in this system:
bot.py: a program that keep receiving user messages from Telegram, and is also responsible for sending response back to the user
image_downloader.py: a program that is responsible for downloading images from either Telegram or a given URL
predict.py: a program that loads a PyTorch pre-trained model for object recognition, and generates predictions when given an image
model details: PyTorch pre-trained InceptionV3 model 
