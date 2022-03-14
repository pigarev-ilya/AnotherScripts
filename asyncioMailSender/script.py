import aiosqlite
import asyncio
import aiosmtplib
from email.message import EmailMessage

async def get_data():
    async with aiosqlite.connect("contacts.db") as connection:
        async with connection.execute('SELECT first_name, email FROM contacts') as cursor:
            contact_list = []
            async for row in cursor:
                contact_list.append(row)
            return contact_list


async def message(name, email):
    message = EmailMessage()
    message["From"] = "ivpigarev@mail.ru"
    message["To"] = "ivpigarev@mail.ru"
    message["Subject"] = "Hello World!"
    message.set_content(f"Уважаемый {name}! Спасибо, что пользуетесь нашим сервисом объявлений.")

    result = await aiosmtplib.send(message, hostname="", port="", use_tls="",
                          username="",
                          password="")
    result = (name, email, result[1])
    return result


async def main():
    contact_list = await get_data()
    coroutined_list = []
    for name, email in contact_list:
        coro = message(name, email)
        coroutined_list.append(coro)
    result = await asyncio.gather(*coroutined_list)
    print(result)


asyncio.run(main())
