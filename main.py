import sys
import speech_recognition as sr
import pyttsx3
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QFileDialog, QLabel

def text_to_speech(text):
    """Конвертує текст у голосове повідомлення."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def speech_to_text():
    """Конвертує голосовий ввід у текст та записує в файл."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Скажіть щось...")
        try:
            audio = recognizer.listen(source, timeout=10)
            text = recognizer.recognize_google(audio, language="uk-UA")

            # Збереження в файл з заголовком - поточний час
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("speech_history.txt", "a", encoding="utf-8") as file:
                file.write(f"{timestamp}\n{text}\n\n")

            return text
        except sr.UnknownValueError:
            return "Не вдалося розпізнати голос."
        except sr.RequestError as e:
            return f"Помилка сервісу: {e}"
        except sr.WaitTimeoutError:
            return "Час очікування на початок голосу минув."

def choose_file_for_speech():
    """Вибір текстового файлу для озвучення."""
    options = QFileDialog.Options()
    file_path, _ = QFileDialog.getOpenFileName(None, "Виберіть текстовий файл", "", "Text files (*.txt);;All files (*)", options=options)
    return file_path

class SpeechApp(QWidget):
    def __init__(self):
        super().__init__()

        # Налаштування основного вікна
        self.setWindowTitle('Голосове перетворення')
        self.setGeometry(100, 100, 500, 400)

        self.layout = QVBoxLayout()

        self.label = QLabel("Виберіть режим роботи:", self)
        self.layout.addWidget(self.label)

        self.button_speech_to_text = QPushButton("Голос у текст", self)
        self.button_speech_to_text.clicked.connect(self.start_speech_to_text)
        self.layout.addWidget(self.button_speech_to_text)

        self.button_text_to_speech = QPushButton("Текст у голос", self)
        self.button_text_to_speech.clicked.connect(self.start_text_to_speech)
        self.layout.addWidget(self.button_text_to_speech)

        self.text_input = QTextEdit(self)
        self.text_input.setPlaceholderText("Введіть текст для озвучення...")
        self.layout.addWidget(self.text_input)

        self.result_text = QTextEdit(self)
        self.result_text.setReadOnly(True)
        self.layout.addWidget(self.result_text)

        self.setLayout(self.layout)

    def start_speech_to_text(self):
        """Обробка та відображення тексту, що був розпізнаний з голосу."""
        text = speech_to_text()
        self.result_text.setPlainText(f"Розпізнаний текст:\n{text}")

    def start_text_to_speech(self):
        """Обробка введеного тексту для озвучення або тексту з файлу."""
        if self.text_input.toPlainText():
            text = self.text_input.toPlainText()
            text_to_speech(text)
        else:
            file_path = choose_file_for_speech()
            if file_path:
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        text = file.read()
                        text_to_speech(text)
                except Exception as e:
                    self.result_text.setPlainText(f"Помилка при читанні файлу: {e}")
            else:
                self.result_text.setPlainText("Файл не був вибраний.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpeechApp()
    window.show()
    sys.exit(app.exec_())