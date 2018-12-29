# loads a PyTorch pre-trained model for object recognition
# generates predictions when given an image
# Auther: Tiger LI
import os
import json
import base64
import requests
from PIL import Image
from redis import StrictRedis
import torchvision.models as models
from torch.autograd import Variable
import torchvision.transforms as transforms

# Initialize pretrained Inception V3 model
model = models.inception_v3(pretrained=True)
model.transform_input = True

# Define the preprocessing function
normalize = transforms.Normalize(
   mean=[0.485, 0.456, 0.406],
   std=[0.229, 0.224, 0.225]
)
preprocess = transforms.Compose([
   transforms.Resize(256),
   transforms.CenterCrop(299),
   transforms.ToTensor(),
   normalize
])
# Download the dictionary of labels
content = requests.get("https://s3.amazonaws.com/deep-learning-models/image-models/imagenet_class_index.json").text
labels = json.loads(content)

r = StrictRedis(host='localhost', port= 6379)

while True:
    print('listening to the queue: image')
    _ , data = r.blpop('image') # _ stands for key: 'download'
    data = data.decode('utf-8')
    chat_id = json.loads(data)['chat_id']
    image_data = json.loads(data)['image']
    #decode image data
    image_data = base64.b64decode(image_data)
    with open('image.png', 'wb') as outfile:
        outfile.write(image_data)

    im = Image.open('image.png')
    img_tensor = preprocess(im)
    img_tensor.unsqueeze_(0)
    img_variable = Variable(img_tensor)

    model.eval()
    preds = model(img_variable)
    # Convert the prediction into text labels

    predictions = []
    for i, score in enumerate(preds[0].data.numpy()):
        predictions.append((score, labels[str(i)][1]))
    # Get the top 5 predictions
    predictions.sort(reverse=True)
    data = {'predictions': [],'chat_id' : chat_id}
    for score, label in predictions[:5]:
        prediction = {'label':label, 'score': '%.4f' % score}
        data['predictions'].append(prediction)

    r.rpush('prediction', json.dumps(data).encode("utf-8"))
    print('get result and sent to queue: prediction')
