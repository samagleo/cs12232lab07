import flet as ft
from flet import TextField

from cs12232lab07lib import authenticate, Session
from cs12232lab07lib.project_types import ChatMessage


async def login() -> Session:
    print('Enter name: ')
    name = input()  # Must have no arguments; Flet issue
    print('Enter password: ')
    password = input()  # Must have no arguments; Flet issue

    try:
        session = await authenticate(name, password, 'ws://oj.dcs.upd.edu.ph:7777/ws')
    except ValueError:
        print('Invalid credentials!')
        exit(1)

    return session


async def app_main(page: ft.Page):
    session = await login()

    chat_field: TextField = TextField(value="", alignment=ft.MainAxisAlignment.CENTER)

    # Change `place_your_callback_here`
    page.run_task(session.make_task(place_your_callback_here))


def main():
    ft.app(app_main)


if __name__ == '__main__':
    main()
