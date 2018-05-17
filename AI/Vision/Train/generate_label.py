# coding: utf-8

import pandas as pd

data = pd.read_csv("./data/train_labels.csv")

data = data.drop_duplicates("class")

data = data.sort_values("class")

id = 1
for i in data["class"][:]:
    f = open("./data/object-detection.pbtxt", "a")
    f.write("item {\n  id: " + str(id) + "\n  name: '" + i + "'\n}\n\n")
    id += 1
    f.close()