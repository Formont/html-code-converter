from aiogram import Bot, Dispatcher, F
from aiogram.types import FSInputFile, Message

import asyncio, os, random

bot = Bot("")

dp = Dispatcher()

def format_pn(number: str) -> str:
    return number.replace("-", "").replace(" ", "")
@dp.message(F.text)
async def message_handler(message: Message):
    end_text = message.text
    if message.entities:
        for entity in message.entities:
            offset, length = entity.offset, entity.length
            sliced = message.text[offset:offset+length+1].strip()
            if entity.type == "italic":
                end_text = end_text.replace(sliced, "<i>"+sliced+"</i>")
            if entity.type == "bold":
                end_text = end_text.replace(sliced, "<b>"+sliced+"</b>")
            if entity.type == "underline":
                end_text = end_text.replace(sliced, "<u>"+sliced+"</u>")
            if entity.type == "strikethrough":
                end_text = end_text.replace(sliced, "<s>"+sliced+"</s>")
            if entity.type == "blockquote":
                end_text = end_text.replace(sliced, "<blockquote>"+sliced+"</blockquote>")
            if entity.type == "code":
                end_text = end_text.replace(sliced, "<code>"+sliced+"</code>")
            if entity.type == "pre":  
                end_text = end_text.replace(sliced, "<pre>"+sliced+"</pre>")
            if entity.type == "text_link":
                end_text = end_text.replace(sliced, f'<a href="{entity.url}">'+sliced+'</a>')
            if entity.type == "url":
                end_text = end_text.replace(sliced, f'<a href="{sliced}">'+sliced+'</a>')
            if entity.type == "phone_number":
                end_text = end_text.replace(sliced, f'<a href="tel:{format_pn(sliced)}">'+sliced+'</a>')
            if entity.type == "email":
                end_text = end_text.replace(sliced, f'<a href="mailto:{sliced}">'+sliced+'</a>')
    paragraphs = end_text.split("\n")
    for p in paragraphs:
        if p:
            end_text = end_text.replace(p, f"<p>{p}</p>")
    fn = f"{message.from_user.id}_{''.join([str(random.randint(0, 9)) for i in range(6)])}.html"
    end_text = end_text.replace("\n\n", "<br>")
    with open(fn, "w+", encoding="utf-8") as file:
        file.write(end_text)
    await message.answer_document(FSInputFile(fn, "result.html"))
    os.remove(fn)

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))