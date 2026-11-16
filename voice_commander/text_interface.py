"""
Text-based REPL interface for testing voice commander commands.
"""

import sys
import os

# Add the current directory to the Python path so we can import modules
sys.path.insert(0, os.path.dirname(__file__))

from core.commands.parser import CommandParser
from core.feedback import Feedback
from core.speech.tts import TTS
from core.actions.launch import Launcher
from core.actions.close import Closer
from core.actions.window import WindowManager

class TextInterface:
    """Text-based REPL interface for testing commands."""

    def __init__(self):
        """Initialize the text interface."""
        self.parser = CommandParser()
        self.feedback = Feedback()
        self.tts = TTS()
        self.launcher = Launcher()
        self.closer = Closer()
        self.window_manager = WindowManager()

        # Set up TTS for feedback
        self.feedback.set_tts(self.tts)

        print("Voice Commander Text Interface")
        print("=" * 30)
        print("Type 'help' for available commands or 'quit' to exit.")
        print("Commands can be entered directly in Russian.")
        print()

    def process_command(self, command_text):
        """
        Process a text command.

        Args:
            command_text (str): Text command to process
        """
        # Parse the command
        parsed_command = self.parser.parse_command(command_text)

        # Handle different command types
        if parsed_command['type'] == 'unknown':
            self.feedback.speak_and_log(f"Неизвестная команда: {command_text}")
            return

        elif parsed_command['type'] == 'help':
            self.show_help()
            return

        elif parsed_command['type'] == 'launch':
            app_name = parsed_command['params'].get('app_name', '')
            result = self.launcher.launch_application(app_name)
            self.feedback.speak_and_log(result['message'])

        elif parsed_command['type'] == 'close':
            app_name = parsed_command['params'].get('app_name', '')
            result = self.closer.close_application(app_name)
            self.feedback.speak_and_log(result['message'])

        elif parsed_command['type'] == 'minimize':
            window_title = parsed_command['params'].get('window_title', '')
            result = self.window_manager.minimize_window(window_title)
            self.feedback.speak_and_log(result['message'])

        elif parsed_command['type'] == 'maximize':
            window_title = parsed_command['params'].get('window_title', '')
            result = self.window_manager.maximize_window(window_title)
            self.feedback.speak_and_log(result['message'])

        elif parsed_command['type'] == 'bring_to_front':
            window_title = parsed_command['params'].get('window_title', '')
            result = self.window_manager.bring_to_front(window_title)
            self.feedback.speak_and_log(result['message'])

        else:
            self.feedback.speak_and_log(f"Команда {parsed_command['type']} не реализована в текстовом интерфейсе")

    def show_help(self):
        """Display help information."""
        help_text = """
Доступные команды (вводите на русском языке):

- Запусти [приложение] - запустить приложение
- Закрой [приложение] - закрыть приложение
- Сверни [окно] - свернуть окно
- Разверни [окно] - развернуть окно
- Прибери [окно] - принести окно вперёд
- Кликни [текст элемента] - кликнуть по элементу интерфейса
- Введи [текст элемента] [текст для ввода] - ввести текст в поле
- Прочти [регион] - прочитать текст с экрана
- Помощь - показать эту справку

Примеры:
- "Запусти блокнот"
- "Закрой браузер"
- "Сверни Chrome"
- "Кликни OK"
- "Введи логин admin"
"""
        self.feedback.speak_and_log(help_text)

    def run(self):
        """Run the text interface REPL loop."""
        print("Готово к вводу команд. Введите 'help' для справки или 'quit' для выхода.")
        print()

        while True:
            try:
                command = input("Введите команду: ").strip()

                if not command:
                    continue

                if command.lower() in ['quit', 'exit', 'выход']:
                    self.feedback.speak_and_log("Завершение работы Voice Commander")
                    break

                # Process the command
                self.process_command(command)

            except KeyboardInterrupt:
                self.feedback.speak_and_log("\nПрограмма завершена пользователем")
                break
            except EOFError:
                # Handle EOF (end of file) - usually happens when input stream is closed
                self.feedback.speak_and_log("Завершение работы Voice Commander")
                break
            except Exception as e:
                self.feedback.speak_and_log(f"Ошибка: {str(e)}")

def main():
    """Main entry point for the text interface."""
    interface = TextInterface()
    interface.run()

if __name__ == "__main__":
    main()