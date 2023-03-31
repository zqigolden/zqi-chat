# Zqi-chat

Zqi-chat is a simple GUI chat application that interacts with OpenAI's GPT-3.5-Turbo model to generate responses based on user input.

## Requirements
To run the application, you will need:

- Python 3 installed on your system
- An OpenAI API key

Installation
1. Clone the project repository: git clone https://github.com/zqigolden/Zqi-chat.git
2. Install required Python modules: pip install pyqt5 openai pyyaml
3. Add your OpenAI API key to a file called api-key.txt.
4. Run the application: python main.py

Usage
1. Enter text into the input field.
1. Select a prompt button to generate a response from the OpenAI GPT-3.5-Turbo model.
1. The generated response will be displayed in the output label.
Notes
- If no prompts.yaml file is present in the project directory, the default prompts will be used. You can add custom prompts in YAML format to this file.
- The font size of the input and output fields can be adjusted from the menu bar.