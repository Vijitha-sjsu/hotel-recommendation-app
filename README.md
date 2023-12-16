# README for Hotel Recommendation App

## Overview
This repository contains the code for a Hotel Recommendation App, an application that recommends hotels based on user input. It is structured into two primary components: a React application for the frontend and a Flask application for the backend.

### React App (Frontend)
The React application serves as the user interface. It collects input parameters from users and displays the results of the hotel recommendation process.

### Flask App (Backend)
The Flask application handles data processing. It preprocesses the input by using a preprocessor and an ensemble model, both obtained from a Colab notebook, to generate hotel recommendations.

## Directory Structure
- **FlaskApp**: Contains the Flask application code, dependencies, preprocessor, and machine learning model.
- **ReactApp**: Contains the React application code and related dependencies.
- **.git**: Git version control directory.

## Setup and Installation
1. **Clone the Repository**: Clone this repository to your local machine.
2. **Install Dependencies**:
   - For React App: Navigate to the React app directory and run `npm install`.
   - For Flask App: Navigate to the Flask app directory and run `pip install -r requirements.txt`.
3. **Starting the Applications**:
   - Run the React app with `npm start`.
   - Run the Flask app with `python app.py` (ensure the Flask environment is activated).

## Usage
- Open the React application in your web browser.
- Input the desired parameters for the hotel search.
- View the recommended hotel clusters displayed by the app.

## Docker Support
If you prefer using Docker, both the React and Flask applications include Dockerfiles. Follow the standard Docker procedures to build and run containers for each part of the application.

## Additional Resources
- **Colab Notebook of the ensemble model(main approach)**: [View Colab](https://colab.research.google.com/drive/1Mgtv7zuU8F-tQZxqQVengiVZxJXEqRyh?usp=sharing)
- **Project Report**: [View Report](https://docs.google.com/document/d/1jB80GH-MP0GFyoXnChJrdWJr2tFsN_qj8E9-ydbRbCI/edit?usp=sharing)
- **CRISP-DM Report**: [View Report](https://docs.google.com/document/d/1dD_71V73G-rWyzwRhZbbkCyz8R6-YHa4ZVmL90DHcCo/edit?usp=sharing)
- **PPT Slide Deck**: [View Slides](https://docs.google.com/presentation/d/1Nw28nkZSgrzF0ougOr9yoQT49979JLGQZ2o3KZKGiEU/edit?usp=sharing)
- **Video Demo**: [View Demo](#) (Link to be added)
- **Alternative Approaches**:
  - [Approach 1](https://colab.research.google.com/drive/1XI0hjYnVMWUw6aNNJSQC48iYSY-BATqQ?usp=sharing)
  - [Approach 2](https://colab.research.google.com/drive/1KWy_-b1b2uG985JOmB764vDnhrwXLHZz?usp=sharing)
  - [Approach 3](https://colab.research.google.com/drive/1fw7utzoeT9pgBMC4OlxAowmaRJQjTEC1)

---
