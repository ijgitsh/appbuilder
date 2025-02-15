# Python app builder

## Overview

This application allows users to generate Python code dynamically using an AI-powered API call. The extracted Python code can be displayed, and users have the ability to toggle its visibility. The app features a simple GUI built with Tkinter.

## Features

Generate Python Code: Users input a prompt, and the application calls an API to generate relevant Python code.

Automatic Code Execution: The extracted Python code can be executed directly within the application.

## Installation

### Prerequisites

- Python 3.x

- Required dependencies listed in requirements.txt

### Steps
1- Clone the repository:

```bash
 git clone https://github.com/ijgitsh/appbuilder.git
cd python-code-generator
```
2- Install dependencies:
```bash
 pip install -r requirements.txt
```

3- Edit API_KEY  variable in the code
```bash
def run_ibm_api(self):
        API_KEY = "<INSERT API KEY>"
```
4- Edit the URL with your agent end point from the deployment space
```bash
            response_scoring = requests.post(
                'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/51373fbb-6f2f-4b78-af5b-8e568d111f1b/ai_service?version=2021-05-01',
                json=payload_scoring,
                headers=header
            )
```

5-Run the application:
```bash
python3.21 app-create-v2.py
```
