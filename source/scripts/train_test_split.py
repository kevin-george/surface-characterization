from sklearn.cross_validation import train_test_split

#Finding all images
images = [os.path.join(root, name) for root, dirs, files in os.walk("./images")
    for name in files if name.endswith((".png"))]

#Spliting it into training and testing groups
#training, testing = train_test_split(images, test_size = 0.5)
training = []
testing = []
for image in images:
    label = image.split("/")[2]
    if label == "aluminium_foil" or label == "brown_bread" or label == "corduroy" or label == "cotton" or label == "cracker" or label == "lettuce_leaf" or label == "linen" or label == "white_bread" or label == "wood" or label == "wool":
        training.append(image)
    else:
        testing.append(image)

label_txt = open("./images/labels.txt", "r")
label_list = {}
for label in label_txt:
    key = label.split(" ")[0]
    value = label.split(" ")[1]
    label_list[key] = value
label_txt.close()

train_txt = open("./images/train.txt", "w")
for imagePath in training:
    label = imagePath.split("/")
    train_txt.write(label[2] + "/" + label[3] + " " + label_list[label[2]])
train_txt.close()

test_txt = open("./images/val.txt", "w")
for imagePath in testing:
    label = imagePath.split("/")
    test_txt.write(label[2] + "/" + label[3] + " " + label_list[label[2]])
test_txt.close()

