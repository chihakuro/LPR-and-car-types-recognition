# LPR-and-car-types-recognition
A small project which involves mainly training models to recognize plate number on cars and utilize it by combining it with car type recognition.

Important Note: 
- Now using state-of-the-art YOLOv9 for recognition. The same process applies.
- Please download the model file before using. https://drive.google.com/file/d/1nAxQkRJD11A227Z8udu03Z02xZXvcQb5/view?usp=drive_link

![Screenshot 2023-07-18 203445](https://github.com/jindaina7734/LPR-and-car-types-recognition/assets/61261926/27c43dcf-57c9-4b7c-88de-614c251e9858)

## I. Introduction

### 1.1 Problem
This is a topic that is also quite popular at the moment. Because this topic is related to security and traffic safety, its importance to real life cannot be denied. In recent years, a lot of data shows that the rate of traffic violations is relatively high, especially since the end of the epidemic, the traffic density is always high, making this number even larger. Therefore, the appearance of security cameras that can recognize license plates is extremely important. By developing this topic and placing it in locations where people often violate traffic rules, license plate information can easily be obtained, thereby obtaining vehicle owner information and having cruel punishment to deter violators.

### 1.2 Goals
The main goal of the project is to classify the type of vehicles and identify their license plates for the purpose of managing the parking lot for a residential area. Moreover, our team expects the project to develop further to recognize the car running on the highway and at the crossroads.

### 1.3 Methodology
The project uses the YOLOv8 algorithm to detect and locate vehicles and license plates in images.

A dataset of around 10,000 images was collected to train the model. 

![Screenshot 2023-07-18 203905](https://github.com/jindaina7734/LPR-and-car-types-recognition/assets/61261926/9557bbab-9656-4c25-99ab-fba7c8874ed8)
This is Car_long & GreenPark dataset. 
About Car_long dataset: This dataset contains photos taken from the garage of a shopping mall. Small in quantity, not rich in shooting angles, many photos of poor quality. 
About GreenPark dataset: Photos of motorbikes and license plates of the shopping mall parking lot. The photos taken are quite clear. However, the quantity isn't much, the rotation angle is still limited and there are some blurred images.


![Screenshot 2023-07-18 203946](https://github.com/jindaina7734/LPR-and-car-types-recognition/assets/61261926/f01c7480-7a83-44cf-b488-409a32148315)
This is CarTGMT dataset: Includes hand-made photographs containing the head/tail of a car with a license plate or motorcycle with a license plate. The advantage is that there are a large number of photos, different angles of the pictures, and a variety of shooting environments.
There are still some repeated images. Photos in dark, rainy environments are a plus. At a certain level, it will become grit that needs to be removed.


![Screenshot 2023-07-18 204038](https://github.com/jindaina7734/LPR-and-car-types-recognition/assets/61261926/d0b6927a-fd12-4bb2-a5ae-1014e723c063)
This is MB10000 dataset: Consisting of 10,000 frames of images extracted from a security camera recording a scene of a one-way street during rush hour. This is an ideal dataset for any recognition model. When it contains a lot of objects in an image with enough resolution to be read.


Now begin with the label process:
![image](https://github.com/jindaina7734/LPR-and-car-types-recognition/assets/61261926/0aa0d657-918e-4590-9f28-bd281830e7cb)
![image](https://github.com/jindaina7734/LPR-and-car-types-recognition/assets/61261926/348feaa4-6409-479b-b1f0-a1c7423ee308)


Then we head to training part. After trained, the model detects objects and provides bounding box coordinates for license plates:
![Screenshot 2023-07-18 205434](https://github.com/jindaina7734/LPR-and-car-types-recognition/assets/61261926/ff740ddb-ee09-4906-bba3-b79bdac54a56)


EasyOCR - an optical character recognition tool was used to extract characters from the license plate images to improve accuracy. The output is a string representing the license plate number:
![Screenshot 2023-07-18 205711](https://github.com/jindaina7734/LPR-and-car-types-recognition/assets/61261926/1e37eb43-6f9a-4d8b-8326-772a3ae9c737)


### 1.4 Conclusion
Paragraph for the training phase:
![Screenshot 2023-07-18 210241](https://github.com/jindaina7734/LPR-and-car-types-recognition/assets/61261926/80f5d8e2-0605-48ca-9575-b82cbcc45698)


Paragraph for the OCR phase:
![Screenshot 2023-07-18 210308](https://github.com/jindaina7734/LPR-and-car-types-recognition/assets/61261926/06484fe5-44b5-4a35-9337-8b87cd834c3c)


How all of things work:
![Screenshot 2023-07-18 210159](https://github.com/jindaina7734/LPR-and-car-types-recognition/assets/61261926/941a1105-9171-457c-9147-2cd2ebe9a123)


## II. Installation:
### 1. Requirement libraries:
First we have to install these libraries (or install through requirements.txt):
```bash
pip install numpy
pip install pandas
pip install opencv-python
pip install ultralytics
pip install easyocr
pip install Pillow
```
```bash
pip install -r requirements.txt
```

### 2. After that:
Run the ```lpr.py``` and then run.

## III. Results:
![Screenshot 2023-07-18 211237](https://github.com/jindaina7734/LPR-and-car-types-recognition/assets/61261926/26901d95-f514-4601-9c4d-66ff82c84f53)
