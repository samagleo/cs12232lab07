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

    async def send_message(e) -> None:
        msg = chat_field.value
        if dm_btn.value:
            dst = recipient_field.value
            recipients = dst.split(',')
            recipients = [i.strip() for i in recipients]
            for i in recipients:
                session.send_direct_message(msg, i)
        else:
            session.send_group_chat_message(msg)

    def dm_box_changed(e) -> None:
        if dm_btn.value:
            recipient_field.disabled = False
        else:
            recipient_field.disabled = True
        page.update()

    def new_message(i) -> None:
        nonlocal chat_history
        chat_history.append(i)
        if i.dst == None:
            lv.controls.append(ft.Text(f'{i.src}: {i.msg}'))
        else:
            lv.controls.append(ft.Text(f'(DM){i.src} ({i.dst}): {i.msg}'))

        page.update()

    async def filter_messages(e) -> None:
        nonlocal chat_history
        keyword = search_field.value
        filtered_chat_history = list(filter(lambda x: keyword in x.msg, chat_history))
        print(filtered_chat_history)
        lv.controls = []

        for i in filtered_chat_history:
            if i.dst == None:
                lv.controls.append(ft.Text(f'{i.src}: {i.msg}'))
            else:
                lv.controls.append(ft.Text(f'(DM){i.src} => {i.dst}: {i.msg}'))

        page.update()


    chat_field: TextField = TextField(value="")
    send_btn: ft.OutlinedButton = ft.OutlinedButton(text="Send", on_click=send_message)
    dm_btn: ft.Checkbox = ft.Checkbox(label="DM?", value=False, on_change=dm_box_changed)
    recipient_field: TextField = TextField(value="Recipient(s)", disabled=True)
    search_field: TextField = TextField(value="Search...")
    search_btn: ft.OutlinedButton = ft.OutlinedButton(text="Search!", on_click=filter_messages)

    chat_history = session.chats

    lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

    for i in chat_history:
        if i.dst == None:
            lv.controls.append(ft.Text(f'{i.src}: {i.msg}'))
        else:
            lv.controls.append(ft.Text(f'(DM){i.src} => {i.dst}: {i.msg}'))


    page.add(
        chat_field, send_btn,
        ft.Row(
            [dm_btn, recipient_field],
        ),
        ft.Row(
            [search_field, search_btn]
        ),
        lv
    )

    # Change `place_your_callback_here`
    page.run_task(session.make_task(new_message))


def main():
    ft.app(app_main)


if __name__ == '__main__':
    main()
