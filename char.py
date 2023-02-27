from ultralytics import YOLO
from pathlib import Path

def char(inp):
    content = []
    bbox = []
    index = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',\
              'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    content_str = []
    char = YOLO(Path(__file__).with_name('char.pt'))
    plate = char.predict(show=True, source=inp, stream=False)
    for result in plate:
        for i in result:
            i = i.boxes.boxes
            # Get the bounding box numbers
            for j in i:
                j = j.tolist()
                bbox.append(j)
        # Sort the bounding box numbers
        bbox.sort(key=lambda x: x[0])
        # Create a list of the 6th element of each list (class of bounding box) in the bounding box list
        for k in bbox:
            content.append(k[5])
        # Convert the list of 6th element to a string
        for l in content:
            l = int(l)
            content_str.append(index[l])

    out = ''.join(content_str)
    return out


