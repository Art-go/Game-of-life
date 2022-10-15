import dataclasses
import os

os.chdir("/home/art")


@dataclasses.dataclass
class Command:
    command: str
    args: str = ""

    @classmethod
    def parse(cls, raw_command: str):
        if " " in raw_command:
            return cls(raw_command[:raw_command.index(" ")], raw_command[raw_command.index(" ")+1:])
        else:
            return cls(raw_command)


while True:
    print("===Консольный проводник===")
    print(os.getcwd())
    print("==========================")
    files = next(os.walk('.'))
    for file in files[1]:
        print(file)
    print("==========================")
    for file in files[2]:
        print(file)
    print("==========================")
    command = Command.parse(input("Введите команду: "))
    os.system("clear")
    print(command.command, command.args)
    match command.command:
        case "exit":
            break
        case "cd":
            if os.access(command.args, os.R_OK):
                os.chdir(command.args)
            else:
                print("Нет прав")
        case "mkdir":
            if os.access(".", os.W_OK):
                try:
                    os.makedirs(command.args)
                except OSError as e:
                    print(f"Ты накосячил где то лови ошибку: {e}")
            else:
                print("Нет прав")
        case "rmdir":
            if os.access(".", os.W_OK):
                os.removedirs(command.args)
            else:
                print("Нет прав")
        case _:
            print("Нет такой команды!")
