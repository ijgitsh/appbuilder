import tkinter as tk
from tkinter import scrolledtext
import subprocess
import sys
import requests
import json

class CodeExecutorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Code Executor")
        self.root.geometry("800x500")
        
        # Top Input Box
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady=5)
        
        self.input_label = tk.Label(self.input_frame, text="what would you like to crate?:")
        self.input_label.pack(side=tk.LEFT, padx=5)
        
        self.user_input = tk.Entry(self.input_frame, width=50)
        self.user_input.pack(side=tk.LEFT, padx=5)
        
        self.api_button = tk.Button(self.input_frame, text="Create app", command=self.run_ibm_api)
        self.api_button.pack(side=tk.LEFT, padx=5)
        
    def execute_code(self):
        code = self.code_input.get("1.0", tk.END)
        try:
            process = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
            output = process.stdout if process.stdout else process.stderr
        except Exception as e:
            output = str(e)
        
        self.output_display.config(state=tk.NORMAL)
        self.output_display.delete("1.0", tk.END)
        self.output_display.insert(tk.END, output)
        self.output_display.config(state=tk.DISABLED)
    
    def run_ibm_api(self):
        API_KEY = "<INSERT API KEY>"
        user_text = self.user_input.get()
        
        try:
            token_response = requests.post(
                'https://iam.cloud.ibm.com/identity/token',
                data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'}
            )
            mltoken = token_response.json().get("access_token", "")
            header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

            payload_scoring = {"messages": [{"content": user_text, "role": "user"}]}
            response_scoring = requests.post(
                'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/51373fbb-6f2f-4b78-af5b-8e568d111f1b/ai_service?version=2021-05-01',
                json=payload_scoring,
                headers=header
            )

            response_text = response_scoring.text
            print(response_text)
            extracted_code = self.extract_python_code(response_text)

            if extracted_code and extracted_code != "No Python code found.":
                self.execute_code_directly(extracted_code)  # Directly execute the code
            else:
                print("No valid Python code extracted.")
        except Exception as e:
            print("Error during API call:", str(e))

    def execute_code_directly(self, code):
        print("executing the code directly")
        """Executes the extracted Python code dynamically."""
        try:
            exec(code, globals())  # Directly execute the code in global context
        except Exception as e:
            print("Error executing extracted code:", str(e))


    def extract_python_code(self, response_text):
        """Extracts Python code from the API response."""
        try:
            parsed_data = json.loads(response_text)
            choices = parsed_data.get("choices", [])
            if choices:
                message_content = choices[0].get("message", {}).get("content", "")
                if message_content.startswith(" ```python") and message_content.endswith("```"):
                    python_code = message_content[10:-3].strip()
                    return python_code
            return "No Python code found."
        except json.JSONDecodeError as e:
            print("JSON Decode Error:", e)
        except Exception as e:
            print("Error extracting Python code:", str(e))
        return "No Python code found."







if __name__ == "__main__":
    root = tk.Tk()
    app = CodeExecutorApp(root)
    root.mainloop()
