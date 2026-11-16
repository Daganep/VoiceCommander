"""
Text-based interface for testing Voice Commander commands without audio input.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.commands.parser import CommandParser
from core.feedback import speak_and_log
from core.logger import get_logger

logger = get_logger(__name__)

def main():
    """Main text interface for testing commands."""
    print("Voice Commander - Text Interface")
    print("Type 'quit' or 'exit' to stop")
    print("Type 'help' for available commands")
    print("-" * 40)

    parser = CommandParser()

    while True:
        try:
            command_text = input("Введите команду: ").strip()

            if command_text.lower() in ['quit', 'exit']:
                speak_and_log("Завершение работы")
                break

            if command_text.lower() == 'help':
                print("Доступные команды:")
                print("- Запустить приложение [имя]")
                print("- Закрыть приложение [имя]")
                print("- Максимизировать окно")
                print("- Минимизировать окно")
                print("- Восстановить окно")
                print("- Перевести окно в фокус")
                print("- Прочитать текст с экрана")
                print("- Кликнуть на [текст]")
                print("- Ввести в поле [текст]")
                print("- Помощь")
                print("- Выход")
                continue

            if command_text:
                # Parse and execute the command
                command = parser.parse_command(command_text)

                if command:
                    result = command.execute()
                    speak_and_log(f"Выполнено: {result}")
                else:
                    logger.warning(f"Unknown command: {command_text}")
                    speak_and_log("Не понял, повторите")

        except KeyboardInterrupt:
            print("\nЗавершение работы")
            break
        except Exception as e:
            logger.error(f"Error in text interface: {e}")
            speak_and_log("Произошла ошибка")

if __name__ == "__main__":
    main()