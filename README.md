# LPR-and-car-types-recognition
A small project which involves mainly on training models to recognize plate number on cars and ultilize it by combining with cars type recognition.
1. Introduction

### 1.1 Problem
This is a topic that is also quite popular at the moment. Because this topic is related to security and traffic safety, it cannot be denied its importance to real life. In recent years, a lot of data shows that the rate of traffic violations is quite high, especially since the end of the epidemic, the traffic density is always high, making this number even larger. Therefore, the appearance of security cameras that can recognize license plates is extremely important. By developing this topic and placing it in locations where people often violate traffic rules, license plate information can easily be obtained, thereby obtaining vehicle owner information and have cold punishment to deter violators.

### 1.2 Goals
The main goal of the project is to classify the type of vehicle and identify their license plates for the purpose of managing the parking lot for a residential area. Moreover, our team expects the project to develop further to recognize the car running on the highway and at the crossroads.

### 1.4 Methodology
The project uses the YOLOv8 algorithm to detect and locate vehicles and license plates in images. A dataset of around 10,000 annotated images was collected to train the model. After training, the model detects objects and provides bounding box coordinates for license plates. EasyOCR - an optical character recognition tool was used to extract characters from the license plate images to improve accuracy. The output is a string representing the license plate number. 


