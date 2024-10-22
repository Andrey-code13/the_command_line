import argparse
from VFS import Virtual_System



def help_text():
    return """
Доступные команды:
- **cd <путь>**: Изменить текущий каталог на "<путь>".
- **ls {опция} [каталог]**: Вывод списка содержимого указанного каталога или текущего каталога, если каталог не указан. Если на месте опции указано -l, то выводится подробная информация.
- **pwd**: Вывод текущего рабочего каталога.
- **tac "имя файла"**: Выводит содержимое файла в обратном порядке с заданным названием в текущем каталоге.
- **chmod [права] <путь>**: Меняет права указанного файла на новые
- **exit**: Завершить сеанс командной строки и возвращает управление терминалу.
- **help**: Отобразить текст справки с кратким описанием всех доступных команд.
"""


def shell(vfs):
    while True:
        print("\033[32m{}".format(f"{vfs.current_dir}$ "),end="")
        line = input().strip()
        if not line:
            continue
        parts = line.split()
        command = parts[0]
        args = parts[1:]

        if command == "exit":
            break

        elif command == "pwd":
            print("\033[33m{}\033[0m".format(vfs.pwd()))

        elif command == "cd":
            if len(args) == 1:
                vfs.cd(args[0])
            else:
                print("Возможно вы некорректно используете команду cd.")
                print("Использование: cd <path>")
                print("Изменить текущий каталог на <path>")
        elif command == "ls":
            if len(args) == 0 or (len(args) == 1 and args[0]=='-l'):
                path, directory_dict = vfs.ls()
            elif len(args) == 1 :
                path, directory_dict = vfs.ls(args[0])
            elif len(args) == 2 and args[0]=='-l':
                path, directory_dict = vfs.ls(args[1])
            else:
                print("Возможно вы некорректно используете команду ls.")
                print("Использование: ls {option} [directory]")
                print("Если введена опция -l выводится подробная информация")
                print("Выводится содержимое текущего каталога, если каталог не указан.")
                print("Выводится содержимое указанного каталога, если каталог указан.")
                continue

            if directory_dict is None:
                print("\033[31m{}\033[0m".format(f"ls: {path}: такого каталога нет"))
            else:
                if(len(args) >0 and args[0]=='-l'):
                    output = []
                    for filename, file_info in directory_dict.items():
                        file_type = file_info["type"]
                        access_rights = file_info["access_rights"]
                        output.append(f"{access_rights}\t{file_type}\t{filename}")
                    print("\033[33m{}\033[0m".format("\n".join(sorted(output))))
                else:
                    print("\033[33m{}\033[0m".format("\n".join(sorted([keys for keys in directory_dict]))))
        elif command == "tac":
            if len(args) == 1:
                lines=vfs.tac(args[0])
                for line in reversed(lines):
                    print("\033[36m{}\033[0m".format(line.strip().decode()))
            else:
                print("Возможно вы некорректно используете команду tac.")
                print("Использование: tac 'Название файла'")
                print("Выводится содержимое файла, который указан.")
                continue
        elif command == "chmod":
            if len(args) == 2:
                if len(args[0]) != 3 or not args[0].isdigit() or int(args[0][0])>7 or int(args[0][1])>7 or int(args[0][2])>7:
                    print("\033[31m{}\033[0m".format(f"chmod: Неверный формат прав доступа. Используйте 'XXX', где X - цифра от 0 до 7."))
                    continue
                if args[1][-1]=='/':
                    print("\033[31m{}\033[0m".format(f"chmod: Путь неоднозначно указывает файл или каталог"))
                    continue
                vfs.chmod(args[0],args[1])
            else:
                print("Возможно вы некорректно используете команду chmod.")
                print("Использование: chmod [права] <путь>")
                print("Изменяются права доступа к файлу на указанные")
                continue
        elif command == "help":
            print("\033[33m{}\033[0m".format(help_text()))

        else:
            print("\033[31m{}\033[0m".format("Неизвестная команда"))
    print("\033[36m{}\033[0m".format("До новых встреч!!!"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Эмулятор оболочки с виртуальной файловой системой.")
    parser.add_argument("zip_path", help="Путь к zip-файлу, содержащему виртуальную файловую систему.")
    args = parser.parse_args()
    vfs = Virtual_System(args.zip_path,)
    shell(vfs)


