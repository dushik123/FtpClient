import ftplib
import os


def connect():
    try:
        auth_ip = input("Введите ip/хост:\n> ")
        auth_login = input("Введите имя пользователя:\n> ")
        auth_pass = input("Введите пароль:\n> ")
        ftp = ftplib.FTP(auth_ip, timeout=10)
        ftp.login(user=auth_login, passwd=auth_pass)
    except:
        print("Вы ввели неверные данные!")
        return None

    print("Вы успешно подключились!")
    data = ftp.retrlines("list")
    ftp.encoding = "utf-8"
    print(data)
    print("Введите -help или -h для справки.")

    return ftp


def rn_funcs(ftp):
    res = "Успешно"
    try:
        rn_name = input("[RN]Введите название файла/каталога:\n> ")
        rn_rename_name = input("[RN]Введите новое название:\n> ")
        ftp.rename(rn_name,rn_rename_name)
    except:
        res = "Такого файла/каталога не существует."
    return res


def upl_funcs(ftp):
    res = "Успешно"
    try:
        upl_name = input("[UPL]Введите название файла:\n> ")
        with open("local_data/"+upl_name, "r+") as file:
            ftp.storbinary(f"STOR {upl_name}", file)
    except:
        res = "Такого файла не существует."
    return res


def delf_funcs(ftp):
    res = "Успешно"
    try:
        delf_name = input("[DELF]Введите название файла:\n> ")
        ftp.delete(delf_name)
    except:
        res = "Такого файла не существует"
    return res


def dw_funcs(ftp):
    res = "Успешно"
    try:
        dw_name = input("[DW]Введите название файла:\n> ")
        with open("download_data/"+dw_name, "wb") as file:
            ftp.retrbinary(f"RETR {dw_name}", file.write)
    except:
        res = "Такого файла не существует."
    return res


def lsl_funcs():
    path_local = "local_data"
    for file in os.listdir(path_local):
        print(file)


def bc_funcs(ftp):
    ftp.cwd("../")
    return "Успешно"


def mkd_funcs(ftp):
    res = "Успешно"
    try:
        mkd_name = input("[MKD]Введите название каталога:\n> ")
        ftp.mkd(mkd_name)
    except:
        res = "Данное название уже существует."

    return res


def delc_funcs(ftp):
    res = "Успешно"
    try:
        delc_name = input("[DELC]Введите название каталога:\n> ")
        ftp.rmd(delc_name)
    except Exception as error:
        print(error)
        res = "Такого каталога не существует."
    return res


def op_funcs(ftp):
    res = "Успешно"
    try:
        op_name = input("[OP]Введите название каталога:\n> ")
        ftp.cwd(op_name)
    except:
        res = "Такого каталога не существует."
    return res


def ls_funcs(ftp):
    data = ftp.retrlines("list")
    return data


def check():
    pass


HELP_TEXT = """
    ls  -   Вывести текущий каталог файлов.
    mkd -   Создать каталог.
    op  -   Открыть каталог.
    delf -  Удалить файл.
    delc -  Удалить каталог.
    bc  -   Вернутся назад.
    lsl -   Вывести каталог локальных файлов.(Папка local_data)
    dw  -   Скачать файл.
    upl -   Закинуть файл (Только из локальной папки).
    rn  -   Переминовать файл/каталог.
    """

COMMANDS = {
    "ls": ls_funcs,
    "op": op_funcs,
    "delc": delc_funcs,
    "mkd": mkd_funcs,
    "bc": bc_funcs,
    "dw": dw_funcs,
    "upl": upl_funcs,
    "delf": delf_funcs,
    "rn": rn_funcs
}


if __name__ == '__main__':
    conn = None

    while conn == None:
        conn = connect()

    while True:
        command = input("> ").lower().strip()

        if command == "-help" or command == "-h":
            print(HELP_TEXT)
            check()
        elif command == 'lsl':
            lsl_funcs()
        elif command in COMMANDS:
            print(COMMANDS[command](conn))
        else:
            print("Неизвестная команда")
            check()