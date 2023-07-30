import optparse
import hashlib
import time
import sys
import string
import random

import pyperclip
import termcolor


# IMPORTANT! Добавить обстрактный класс для интерфейса:
class CLInterface:
    def __init__(self) -> None:
        self.__parser = optparse.OptionParser()

        self.passphrase_control = Passphrase()
        # Добавляем опции для cli
        self.__parser.add_option(
            "-p",
            "--password",
            dest="password",
            type="str",
            help=("Легкий пароль, который легко запомнить"),
        )

        self.__parser.add_option(
            "-s",
            "--static",
            dest="static",
            help=("Неизменяемые данные, обычно - название сервиса "),
        )

        self.__parser.add_option(
            "-c",
            "--passphrase",
            dest="passphrase",
            default="",
            type="str",
            help=(
                "Ваша кодовая фраза для генерации пароля > 8 символов "
                "[default: %default]"
            ),
        )

        self.__parser.add_option(
            "-S",
            "--save",
            dest="save",
            action="store_true",
            default=False,
            help=("Сохранить кодовую фразу"),
        )

        self.__parser.add_option(
            "-b",
            "--beta",
            dest="beta",
            action="store_true",
            default=False,
            help=("Использовать бета-версию"),
        )

        # Установка параметров по умолчанию и парсинг переданных аргументов
        self.__parser.set_defaults(passphrase=self.passphrase_control.passphrase)
        self._opts, self._args = self.__parser.parse_args()
        self.passphrase = self._opts.passphrase

    @property
    def password(self):
        if self._opts.password:
            return self._opts.password
        return CLIDecor.serial_input("Password: ", 0.1, "green")

    @property
    def static(self):
        if self._opts.static:
            return self._opts.static.lower()
        return CLIDecor.serial_input("Static: ", 0.1, "green")

    @property
    def passphrase(self):
        return self.passphrase_control.passphrase

    @passphrase.setter
    def passphrase(self, value):
        self.passphrase_control.passphrase = value
        # Если фраза прошла проверку
        if self.passphrase_control.passphrase:
            if self._opts.save:
                self.passphrase_control.save()

    @property
    def beta_version(self):
        return self._opts.beta


class Passphrase:
    def __init__(self, path_to_passphrase: str = "passphrase.txt") -> None:
        self.__passphrase = ""
        self.path_to_passphrase = path_to_passphrase

    @property
    def passphrase(self):
        if not self.__passphrase:
            with open(self.path_to_passphrase, "r", encoding="utf-8") as file:
                self.__passphrase = file.readline()
                if not self.__passphrase:
                    print("Нет сохраненной кодовой фразы\n-h | --help для документации")
        return self.__passphrase.lower().strip()

    @passphrase.setter
    def passphrase(self, phrase: str):
        if isinstance(phrase, str):
            self.__passphrase = phrase
        else:
            print("Кодовая фраза не поддерживается")

    def save(self):
        with open(self.path_to_passphrase, "w", encoding="utf-8") as file:
            file.write(self.__passphrase)


class Hestale:
    # Генерируем кодовую фразу хеш-функцией sha256, и возвращаем первые 20 символов
    @staticmethod
    def generate_key_from_phrase(phrase):
        sha256 = hashlib.sha256()
        sha256.update(phrase.encode())
        return sha256.hexdigest()[:20]

    @staticmethod
    def mix_words(word1, word2, key):
        #  Преобразуем данные к длине ключа
        while len(key) > len(word1):
            word1 += word1

        while len(key) > len(word2):
            word2 += word2

        word1 = word1[: len(key)]
        word2 = word2[: len(key)]

        # преобразуем слова и ключ в бинарный формат
        word1_bin = "".join(format(ord(c), "08b") for c in word1)
        word2_bin = "".join(format(ord(c), "08b") for c in word2)
        key_bin = "".join(format(ord(c), "08b") for c in key)

        # выполняем операцию XOR над каждым битом
        mixed_bin = "".join(
            str(int(word1_bin[i]) ^ int(word2_bin[i]) ^ int(key_bin[i]))
            for i in range(len(key_bin))
        )

        # преобразуем результат обратно в строку
        mixed_str = "".join(
            chr(int(mixed_bin[i : i + 8], 2)) for i in range(0, len(mixed_bin), 8)
        )
        return mixed_str


class Control:
    def __init__(self, interface) -> None:
        self.__password = interface.password
        self.__static = interface.static
        self.__passphrase = interface.passphrase
        self.__beta_version = interface.beta_version

    def get_password(self):
        if self.__beta_version:
            from hestale_beta import create_password

            return create_password(self.__password, self.__static)

        password = Hestale.mix_words(
            self.static,
            self.password,
            Hestale.generate_key_from_phrase(self.passphrase),
        )
        pyperclip.copy(password)
        return password

    @property
    def password(self):
        return self.__password

    @property
    def static(self):
        return self.__static

    @property
    def passphrase(self):
        return self.__passphrase


class CLIDecor:
    @classmethod
    def serial_input(
        cls, text: str, interval: float = 0.5, color: str = "yellow"
    ) -> str:
        for char in text:
            time.sleep(interval)
            sys.stdout.write(termcolor.colored(char, color=color))
            sys.stdout.flush()
        return input()
    
    @classmethod
    def serial_output(
        cls, text: str, interval: float = 0.5, color: str = "yellow"
    ) -> None:
        for char in text:
            time.sleep(interval)
            sys.stdout.write(termcolor.colored(char, color=color))
            sys.stdout.flush()

    @classmethod
    def shuffle_output(
        cls, text: str, interval: float = 0.1, color: str = "green"
    ) -> None:
        for i in range(len(text) + 1):
            random_letters = list(string.ascii_letters)
            random.shuffle(random_letters)
            for random_char in random_letters[: random.randint(2, 5)]:
                time.sleep(interval)
                sys.stdout.write(
                    "\r"
                    + termcolor.colored(text[:i], color=color)
                    + termcolor.colored(
                        random_char if i < len(text) else "", color="red"
                    )
                )
                sys.stdout.flush()


if __name__ == "__main__":
    cli = CLInterface()
    control = Control(interface=cli)
    
    CLIDecor.serial_output('-- Your Password --', interval = 0.1, color = 'blue')
    CLIDecor.shuffle_output(control.get_password())
    print()
    CLIDecor.serial_input("Enter for exit..", 0.1, "magenta")
