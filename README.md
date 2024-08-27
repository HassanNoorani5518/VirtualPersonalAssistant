# AI-Powered Virtual Fitness Assistant Project

## Team Members:
- Duranni Wright 
- Hassan Noorani 
- Hadi
- Jordyn

## Table of Contents
1. [Abstract](#abstract)
2. [Introduction](#introduction)
3. [System Design](#system-design)
4. [User Interaction Design](#user-interaction-design)
5. [Iterative Development](#iterative-development)
6. [Implementation](#implementation)
7. [Testing and Evaluation](#testing-and-evaluation)
8. [Discussion and Conclusion](#discussion-and-conclusion)
9. [References](#references)

## Abstract
Our Fitness Assistant is a smart embedded system designed to track workouts, specifically bicep curls and squats. The system utilizes pose detection software to ensure proper form, thereby allowing the user to maximize their productivity while working out. The Fitness Assistant is built using a Raspberry Pi 4, Coral USB AI Accelerator, and a 720p USB webcam.

## Introduction

### Problem Statement:
Gym-goers often lose motivation when they do not see progress for their hard work. A Fitness Assistant that encourages proper form can help users achieve their goals faster. Incorrect workouts not only produce minimal results but can also lead to injuries.

### Project Objectives:
The Fitness Assistant should capture the user's movements and accurately determine if the workout was performed correctly. It should also communicate with the user to inform them of the number of reps completed. Additionally, the assistant should offer the option to switch between exercises and reset counters as desired.

## System Design

### Hardware Architecture:
The Raspberry Pi 4 serves as the base processing unit. The Coral Accelerator is used to handle the heavy load of AI models, a USB camera is used for input, and the Sense HAT is used for visual feedback.

### Software Architecture:
The system's architecture is structured with a flowchart or diagram outlining the modules and data flow. This includes key software libraries/frameworks used (TensorFlow, OpenCV, etc.), algorithms for exercise/pose recognition, speech recognition, and natural language processing.

#### **Key Components:**
- **gemini.py**: 
  - This module is responsible for handling speech recognition and communicating with the Gemini AI model. It captures speech input from the user, processes it using Google Web Speech API, and then sends the recognized text to the Gemini AI model. Based on the response from Gemini, it returns the appropriate command related to the exercise (e.g., "curls," "squats," "reset," "quit").

- **inference.py**:
  - This module handles the core inference logic for processing images through the MoveNet pose detection model. It includes functions to preprocess images and run inferences using either a TPU or CPU, depending on the hardware setup.

- **visualization.py**:
  - This module is responsible for visualizing the keypoints detected by the MoveNet model. It draws the detected landmarks and exercise counts on the video feed and updates the Sense HAT LED display with the current exercise count.

- **exercises.py**:
  - This module defines the logic for counting bicep curls and squats based on the detected keypoints. It includes classes for each exercise, with methods to process keypoints, count repetitions, and reset counters.

- **fitness_core.py**:
  - This module serves as the central hub for shared functions, constants, and variables used throughout the project. It defines core functionality such as setting up the Sense HAT, configuring key constants like confidence thresholds, and other utility functions.

- **main.py**:
  - This is the entry point of the project, orchestrating the initialization of all components and handling the main loop. It captures video input, processes it through the inference and exercise logic, and manages the threads for fitness activity monitoring and command listening.

## User Interaction Design

### Interface Design:
Users interact with the assistant via the USB webcam (with a built-in microphone). The MoveNet pose detection model places landmarks on the user's image to track their movements. The assistant is controlled by voice commands recorded through the USB camera’s microphone. Speech recognition software transcribes voice into text, which is then sent to Google’s Gemini API to determine the user's intent. The response from Gemini is used to manipulate the program based on the user’s command.

### Feedback Mechanism:
Feedback is provided to the user via the Sense HAT 8x8 LED matrix, allowing users to see if they are executing exercises correctly.

## Iterative Development

### Prototype Stages:
The early iterations of the program used the MediaPipe pose detection model and focused on one arm while we developed the logic for counting reps. We later switched to the MoveNet pose detection model, implemented logic for both arms, and introduced the logic for squats.

### Feedback Loops:
We used OpenCV to visualize what our pose detection models were capturing and to check accuracy.

### Design Iterations:
Key changes made through our iterations included adapting landmark validation and switching from the MoveNet Lightning model to the MoveNet Thunder model.

### Lessons Learned:
We learned a great deal from this project, particularly the Python programming language, which was new to us but simple to learn. We also learned how to adopt open-source models into our projects and how to implement APIs.

## Implementation

### Computer Vision:
The MoveNet model was employed for pose estimation, with pre-trained weights optimized for Edge TPU and CPU processing. This system was used to recognize the exercises.

### Speech Recognition:
Google Web Speech API was integrated to handle voice commands, which were processed by Gemini to determine the correct action.

### System Integration:
We integrated vision, speech, and NLP modules on the Raspberry Pi with Python code, as well as the Coral AI Accelerator, to ensure real-time cohesion.

## Testing and Evaluation

### Metrics:
System performance was measured by tracking FPS and response time to commands. We used OpenCV to monitor landmark positioning and set print statements to display messages in the terminal.

### Testing Procedures:
Our modules were tested during lab sessions before being implemented into our project. The final system was tested with users performing exercises in different environments to ensure robustness and accuracy.

## Discussion and Conclusion

### Lessons Learned:
The project highlighted the importance of balancing processing power and accuracy, especially in resource-constrained environments like the Raspberry Pi 4.

### Future Work:
Potential improvements include increasing the number of exercise capabilities, improving program accuracy, and redesigning the user interface for better feedback and interaction.

### Ethical Considerations:
Given that the main input is a camera, privacy was a major concern. Our program handles data processing locally, with the exception of using the Gemini chatbot.

## References
- TensorFlow Lite documentation
- Google Generative AI (Gemini) API
- Raspberry Pi and Coral USB Accelerator documentation
- OpenCV and Python libraries for image processing
