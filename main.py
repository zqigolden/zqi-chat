import openai
from PyQt5.QtWidgets import QApplication, QTextEdit,\
    QPushButton, QMenuBar, QAction, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from functools import partial
import yaml

try:
    with open('api-key.txt', 'r') as f:
        file_content = [i.strip() for i in f.readlines() if not i.startswith('#')]
        print(file_content)
        openai.api_key = file_content[0] if len(file_content) == 1 else ''.join(file_content)
except FileNotFoundError:
    with open('api-key.txt', 'w') as f:
        f.write('# Please add your OpenAI API key here.\n')
    raise RuntimeError('Please create a file called api-key.txt and add your OpenAI API key to it.')

PROMPTS = {
    '对话': 'Chat freely with me'
}

try:
    with open('prompts.yaml', 'r', encoding='utf-8') as f:
        PROMPTS.update(yaml.safe_load(f))
    print(PROMPTS)
except FileNotFoundError:
    pass

MESSAGES = []


class Translator(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle('Zqi-chat')

        # Add menu bar
        menu_bar = QMenuBar()
        self.setMenuBar(menu_bar)

        # Add font size menu with actions to adjust labels
        font_size_menu = menu_bar.addMenu('Font Size')
        font_sizes = [('Tiny', 10), ('Small', 14), ('Medium', 18), ('Large', 24), ('Huge', 32)]
        self.font_sizes = {k: v for (k, v) in font_sizes}
        for name, size in font_sizes:
            action = QAction(name, self)
            action.triggered.connect(partial(self.set_font_size, size))
            font_size_menu.addAction(action)
        
        # Add input text area
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText('Enter text here...')
        self.input_text.setMinimumHeight(100)
        self.input_text.setMinimumWidth(800)
        self.input_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        # Add output label
        self.output_label = QTextEdit()
        self.output_label.setReadOnly(True)
        self.output_label.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.output_label.setMinimumHeight(100)
        self.output_label.setMinimumWidth(800)

        # Clean format of input
        self.input_text_count = 0

        def _clean_input():
            # Save the current cursor position

            target_text = self.input_text.toPlainText().strip()
            if len(target_text) != self.input_text_count:
                cursor_position = self.input_text.textCursor().position()
                self.input_text_count = len(target_text)
                self.input_text.setText(target_text)
                new_cursor = self.input_text.textCursor()
                new_cursor.setPosition(cursor_position)
                self.input_text.setTextCursor(new_cursor)

        self.input_text.textChanged.connect(_clean_input)

        # Add input text area and output label to the layout
        central_widget = self.centralWidget() or QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        layout.addWidget(self.input_text)
        layout.addWidget(self.output_label)

        # Add buttons
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout()
        buttons_widget.setLayout(buttons_layout)
        buttons_layout.addStretch()
        for button_name in PROMPTS.keys():
            button = QPushButton(button_name, self)
            buttons_layout.addWidget(button)
            button.clicked.connect(partial(self.trigger_prompt, button_name))
        layout.addWidget(buttons_widget)

        # Set the central widget
        self.setCentralWidget(central_widget)

    def set_font_size(self, size):
        # Adjust font size of input and output labels based on selected size
        font = QFont('Microsoft YaHei', size)
        gui_font = QFont('Microsoft YaHei', size - 4)
        for widget in self.findChildren(QWidget):
            widget.setFont(gui_font)
        self.input_text.setFont(font)
        self.output_label.setFont(font)

    def trigger_prompt(self, prompt_name):
        # Get input text from GUI and pass to GPT model with the corresponding prompt
        input_text = self.input_text.toPlainText().strip()
        response_text = ask_gpt(PROMPTS[prompt_name], input_text)

        # Update GUI with GPT-generated response
        self.output_label.setText(response_text)


def ask_gpt(prompt, message):
    message = message.strip()
    if len(MESSAGES) > 0:
        last_prompt = [i for i in MESSAGES if i['role'] == 'system'][-1]
        if last_prompt['content'] != prompt:
            MESSAGES.append({'role': 'system', 'content': prompt})
    else:
        MESSAGES.append({'role': 'system', 'content': prompt})

    MESSAGES.append({'role': 'user', 'content': message})
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            max_tokens=2048,
            n=1,
            temperature=0.7,
            messages=MESSAGES,
        )
    except openai.error.AuthenticationError:
        return 'API key error. Please check your OpenAI API key.'
    MESSAGES.append(response.choices[0].message)
    return MESSAGES[-1]['content']


if __name__ == '__main__':
    app = QApplication.instance() or QApplication([])
    translator = Translator()
    translator.set_font_size(translator.font_sizes['Small'])
    translator.show()
    app.exec_()
