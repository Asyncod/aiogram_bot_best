# -*- coding: utf-8 -*-
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types, executor, filters
from aiogram.dispatcher import FSMContext

import config
import random
import base
import asyncio
import requests


#### PARAMETRS BOT'S ####
bot = Bot(config.bot_token, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())
admin_id_list = [] # admin list
proger_id = 12345 # id for send error logs


## NEED BASE ##
base.create_db()


#### FSM CLASS ####
class FSM_adv(StatesGroup):
    first_captcha = State()
    add_balance = State()
    add_unik_user = State()
    add_unik_balance = State()


#### NEED CLASS ####
class Setting():
    message_history = []


#### ALL HANDLER'S FUNC ####
async def check_message(user_id): # check user's message
    if (user_id in Setting.message_history):
        return True
    else:
        return False


async def in_chat(message): # check user's chat status
    stats = await bot.get_chat_member(chat_id=config.channel_id, user_id=message.chat.id)
    status = stats.status
    if status == "left":
        return False
    else:
        return True


async def generate_ref(message):
    link = f"https://t.me/{config.channel_referal}?start={message.chat.id}"
    return link


async def referal_widthward(message):
    await asyncio.sleep(5)

    summe = base.get_withdraw(message.chat.id)

    random_list = [1, 2, 4, 5, 6, 7, 8, 9, 0]

    code_text = ""
    for i in range(10):
        code_text += str(random.choice(random_list))

    try:
        answer_post = requests.post(url="https://pay.crypt.bot/api/transfer",
                                    headers={"Host": "pay.crypt.bot",
                                             "Crypto-Pay-API-Token": config.appl_token},
                                    data={"user_id": message.chat.id,
                                          "asset": "TON",
                                          "amount": summe,
                                          "spend_id": code_text,
                                          "comment": "Спасибо за приглашенных людей!"})

        json_answer = answer_post.json()

        with open("logs_ref.txt", "a") as file:
            file.write(f"{json_answer} {message.chat.id} @{message.from_user.username}\n")

        if json_answer["ok"] == True:
            base.cleaning_withdraw(message.chat.id)
            await bot.send_message(chat_id=message.chat.id,
                                   text="На ваш счет зачислен платеж по реферальной системе, спасибо что с нами!")

        elif json_answer["ok"] == False:
            await bot.send_message(chat_id=proger_id,
                                   text=f"<b>⚠ Ошибка!</b>\n\n"
                                        f"<b>Пользователь:</b> {message.from_user.id}\n"
                                        f"<b>Код:</b> <code>{json_answer}</code>")
            print(json_answer)

    except Exception as exec:
        await bot.send_message(chat_id=proger_id,
                               text=f"<b>⚠ Возникла ошибка с интернетом</b>\n\n"
                                    f"Код ошибки <code>{exec}</code>\n\n"
                                    f"Вывод реферальных денег у {message.chat.id}")
        print(json_answer)


async def sleep_wait(message):
    await asyncio.sleep(86400)

    random_list = [1, 2, 4, 5, 6, 7, 8, 9, 0]

    code_text = ""
    for i in range(10):
        code_text += str(random.choice(random_list))

    if (await in_chat(message) == True):
        try:
            answer_post = requests.post(url="https://pay.crypt.bot/api/transfer",
                                        headers={"Host": "pay.crypt.bot",
                                                "Crypto-Pay-API-Token": config.appl_token},
                                       data={"user_id": message.chat.id,
                                             "asset": "TON",
                                             "amount": "0.015",
                                             "spend_id": code_text,
                                             "comment": "Спасибо за подписку!"})

            json_answer = answer_post.json()

            with open("logs.txt", "a") as file:
                file.write(f"{json_answer} {message.chat.id} @{message.from_user.username}\n")

            if json_answer["ok"] == True:
                await bot.send_message(chat_id=message.chat.id,
                                       text="На ваш счет зачислен платеж за подписку, спасибо что с нами!")


            elif json_answer["ok"] == False:
                if json_answer["error"]["name"] == "USER_NOT_FOUND":
                    keyboard = types.InlineKeyboardMarkup()
                    but1 = types.InlineKeyboardButton(text="Проверить еще раз", callback_data="second_check")
                    keyboard.add(but1)

                    await bot.send_message(chat_id=message.chat.id,
                                           text="<b>Для получения вознаграждения необходимо запустить <a href='t.me/CryptoBot?start=r-633430'>@CryptoBot</a></b>\n\n"
                                                "После запуска снова нажмите на кнопку проверки",
                                           reply_markup=keyboard,
                                           disable_web_page_preview=True)

                elif json_answer["error"]["name"] == "SPEND_ID_ALREADY_USED":
                    await bot.send_message(chat_id=proger_id,
                                           text=f"<b>⚠ Ошибка со SPEND_ID, запущена повторая проверка</b>\n\n"
                                                f"<b>Пользователь:</b> {message.from_user.id}\n"
                                                f"<b>Код:</b> <code>{json_answer}</code>")
                    print(json_answer)
                    await sleep_wait(message)

                else:
                    await bot.send_message(chat_id=proger_id,
                                           text=f"<b>⚠ Ошибка!</b>\n\n"
                                                f"<b>Пользователь:</b> {message.from_user.id}\n"
                                                f"<b>Код:</b> <code>{json_answer}</code>")
                    print(json_answer)

        except Exception as exec:
            await bot.send_message(chat_id=proger_id,
                                   text=f"<b>⚠ Возникла ошибка с интернетом</b>\n\n"
                                        f"Код ошибки <code>{exec}</code>\n\n"
                                        f"Вывод денег за подписку у {message.chat.id}")
            print(json_answer)

    elif (await in_chat(message) == True):
        keyboard = types.InlineKeyboardMarkup()
        but1 = types.InlineKeyboardButton(text="Проверить еще раз", callback_data="second_check")
        keyboard.add(but1)

        await bot.send_message(chat_id=message.chat.id,
                               text="<b>Вы не подписаны на канал!</b>\n\n"
                                    "Для зачисления токенов вам надо быть подписаным на канал! После подписки нажмите на кнопку проверки",
                               reply_markup=keyboard)


async def check_user(message):
    answer = base.get_user(message.from_user.id)
    username = message.from_user.username
    name = message.from_user.first_name
    if answer == None:
        base.new_user(id_user=message.from_user.id,
                      username=username,
                      name=name)
    else:
        return True


async def add_invited(message, inviter):
    base.add_invited(message.from_user.id, inviter)


async def new_referal(message, referal_id):
    referal_count = base.get_referal(referal_id)
    if (message.from_user.username != None):
        username = base.get_username(message.from_user.id)
        await bot.send_message(chat_id=referal_id, text=f"Новый реферал @{username}\n"
                                                        f"Рефеалов сейчас: {referal_count}")

    else:
        name = base.get_name(message.from_user.id)
        await bot.send_message(chat_id=referal_id, text=f"Новый реферал {name}\n"
                                                        f"Рефеалов сейчас: {referal_count}")


async def big_og():
    list_lider = base.get_lider()
    big_man = list_lider[0]
    text = f"{big_man[1]} с {big_man[3]} рефералами!"
    return text


async def liders_table():
    list_lider = base.get_lider()
    position = 0
    main_text = "<b>🏆 Таблица лидеров:</b>\n\n"

    if len(list_lider) <= 10:
        for users in list_lider:
            position += 1
            main_text += f"<b>ID: {users[0]}</b>\n" \
                         f"USER: @{users[1]}\n" \
                         f"NAME: {users[2]}\n" \
                         f"COUNT: {users[3]}\n\n"

    else:
        for users in (list_lider[:20]):
            position += 1
            main_text += f"<b>ID: {users[0]}</b>\n" \
                         f"USER: @{users[1]}\n" \
                         f"NAME: {users[2]}\n" \
                         f"COUNT: {users[3]}\n\n"

    return main_text


### MESSAGE HISTORY ####
@dp.message_handler(filters.IDFilter(chat_id=config.chat_id))
async def hand_mess(message: types.Message):
    if (len(Setting.message_history) >= 20):
        Setting.message_history.pop(0)
        Setting.message_history.append(message.from_user.id)

    else:
        Setting.message_history.append(message.from_user.id)


@dp.message_handler(state=FSM_adv.add_balance)
async def hand_mess(message: types.Message, state: FSMContext):
    try:
        if str(message.text).isdigit():
            answer_post = requests.post(url="https://pay.crypt.bot/api/createInvoice",
                                        headers={"Host": "pay.crypt.bot",
                                                 "Crypto-Pay-API-Token": config.appl_token},
                                        data={"asset": "TON",
                                              "amount": message.text})

            need_json = answer_post.json()

            if need_json['ok'] == True:
                keyboard_1 = types.InlineKeyboardMarkup(row_width=1)
                but1 = types.InlineKeyboardButton(text="Оплатить", url=need_json['result']['pay_url'])
                but2 = types.InlineKeyboardButton(text="⬅️ Вернуться", callback_data="back_admin")
                keyboard_1.add(but1, but2)

                await bot.send_message(chat_id=message.chat.id,
                                       text=f"<b>Сумма:</b> {need_json['result']['amount']}\n"
                                            f"<b>Дата создания:</b> {need_json['result']['created_at']}",
                                       reply_markup=keyboard_1,
                                       disable_web_page_preview=True)
                await state.finish()

            else:
                await bot.send_message(chat_id=message.chat.id,
                                       text=f"<b>Ошибка при генерации ссылки для пополения, начните сначала</b>\n\n"
                                            f"<b>Код:</b> <code>{need_json}</code>")
                await state.finish()

        else:
            await bot.send_message(chat_id=message.chat.id,
                                   text="Введите число")

    except Exception as exep:
        keyboard_2 = types.InlineKeyboardMarkup()
        but1 = types.InlineKeyboardButton(text="⬅️ Вернуться", callback_data="back_admin")
        keyboard_2.add(but1)

        await state.finish()
        await bot.edit_message_text(chat_id=message.chat.id,
                                    message_id=message.message_id,
                                    text=f"<b>Ошибка при генерации счета для пополнения баланса</b>\n\n"
                                         f"<b>Код:</b> <code>{exep}</code>",
                                    reply_markup=keyboard_2,
                                    disable_web_page_preview=True)


@dp.message_handler(state=FSM_adv.add_unik_user)
async def add_unik(message: types.Message):
    if str(message.text).isdigit():
        with open("unik_id.txt", "r") as file:
            list_id = file.read().split("\n")

        if message.text not in list_id:
            with open("unik_id.txt", "a") as file:
                file.write(f"{message.text}\n")

            await FSM_adv.add_unik_balance.set()
            await bot.send_message(chat_id=message.chat.id,
                                   text="<i>Теперь отправьте прибавку для этого человека</i>\n\n"
                                        "<b>Например:</b> <code>0.1</code>",
                                   disable_web_page_preview=True)

        else:
            keyboard = types.InlineKeyboardMarkup()
            but1 = types.InlineKeyboardButton(text="⬅️ Вернуться", callback_data="back_admin")
            keyboard.add(but1)

            await bot.send_message(chat_id=message.chat.id,
                                   text="<b>Данный ID уже есть!</b>\n"
                                        "Вернитесь или отправьте другой",
                                   reply_markup=keyboard,
                                   disable_web_page_preview=True)

    else:
        await bot.send_message(chat_id=message.chat.id,
                               text="Введите число")


@dp.message_handler(state=FSM_adv.add_unik_balance)
async def add_balic(message: types.Message, state: FSMContext):
    with open("unik_balance.txt", "a") as file:
        file.write(f"{message.text}\n")

    keyboard = types.InlineKeyboardMarkup()
    but1 = types.InlineKeyboardButton(text="⬅️ Вернуться", callback_data="back_admin")
    keyboard.add(but1)

    await bot.send_message(chat_id=message.chat.id,
                           text="<b>🥵 Все добавлено</b>",
                           reply_markup=keyboard,
                           disable_web_page_preview=True)

    await state.finish()


#### START HANDLERS ####
@dp.message_handler(commands=["start"])
async def starting(message: types.Message):
    user = message.from_user.id
    referal = message.text

    if (referal.find(" ")) != -1:  ## if referal link
        referal_text = int(referal[referal.find(" ") + 1:])
        if (referal_text != user) and (await check_user(message) != True):  ## new referal

            await asyncio.sleep(300)
            base.new_referal(referal_text)
            base.add_balance(referal_text)
            await new_referal(message, referal_text)
            await add_invited(message, referal_text)

            keyboard = types.InlineKeyboardMarkup()
            but1 = types.InlineKeyboardButton(text="Я готов!", callback_data="start")
            keyboard.add(but1)

            await bot.send_photo(chat_id=message.chat.id,
                                 photo="AgACAgIAAxkBAAMFYqMb00Q0qqZbHXqKBs9m0CshA2wAAoe5MRvfvRhJW21iVpt0QCMBAAMCAAN5AAMkBA",
                                 caption="<b>🙋 Привет!</b>\n\n")
            await bot.send_message(chat_id=message.chat.id,
                                   text="<i>🌿 Я телеграмм-бот от криптокомпании <a href='https://t.me/in_rusyaev'>“Русяев и партнёры”</a></i>\n\n"
                                        "За подписку на канал нашей компании мы раздаём бесплатные токены TON, а активные участники нашего канала будут постоянно участвовать в конкурсах, розыгрышах, где мы будем дарить криптовалюту!\n\n"
                                        "<b>💎 Чем больше друзей приведете, тем больше подарков будет!</b>\n\n"
                                        "<i>Ты готов поучаствовать и гарантированно получить на свой кошелёк токены? Тогда начинаем!</i>",
                                   reply_markup=keyboard,
                                   disable_web_page_preview=True)

        else:
            await cabinet(message)

    else: ## if not referal (simple /start)

        if (message.from_user.id in admin_id_list):
            await check_user(message)
            await admin_cabinet(message)

        elif (await check_user(message) == True) and (await in_chat(message) == True):
            await cabinet(message)

        else:
            keyboard = types.InlineKeyboardMarkup()
            but1 = types.InlineKeyboardButton(text="Я готов!", callback_data="start")
            keyboard.add(but1)

            await bot.send_photo(chat_id=message.chat.id,
                                 photo="AgACAgIAAxkBAAMFYqMb00Q0qqZbHXqKBs9m0CshA2wAAoe5MRvfvRhJW21iVpt0QCMBAAMCAAN5AAMkBA",
                                 caption="<b>🙋 Привет!</b>\n\n")
            await bot.send_message(chat_id=message.chat.id,
                                   text="<i>🌿 Я телеграмм-бот от криптокомпании <a href='https://t.me/in_rusyaev'>“Русяев и партнёры”</a></i>\n\n"
                                        "За подписку на канал нашей компании мы раздаём бесплатные токены TON, а активные участники нашего канала будут постоянно участвовать в конкурсах, розыгрышах, где мы будем дарить криптовалюту!\n\n"
                                        "<b>💎 Чем больше друзей приведете, тем больше подарков будет!</b>\n\n"
                                        "<i>Ты готов поучаствовать и гарантированно получить на свой кошелёк токены? Тогда начинаем!</i>",
                                   reply_markup=keyboard,
                                   disable_web_page_preview=True)


async def cabinet(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    but1 = types.InlineKeyboardButton(text="📈 Статистика", callback_data="stat")
    but2 = types.InlineKeyboardButton(text="🔗 Реферальная ссылка", callback_data="ref_link")
    but3 = types.InlineKeyboardButton(text="ℹ️ Правила", callback_data="rule")
    but4 = types.InlineKeyboardButton(text="💸 Запросить вывод", callback_data="money")
    keyboard.add(but2)
    keyboard.add(but1, but3)
    keyboard.add(but4)

    await bot.send_photo(chat_id=message.chat.id,
                         photo="AgACAgIAAxkBAAMFYqMb00Q0qqZbHXqKBs9m0CshA2wAAoe5MRvfvRhJW21iVpt0QCMBAAMCAAN5AAMkBA",
                         caption="<b>🙋 Привет!</b>\n\n")
    await bot.send_message(chat_id=message.chat.id,
                           text=f"<b>Это твой кабинет</b>\n\n"
                                f"Здесь ты можешь получить реферальну ссылку, изучить правила, проверить количество приглашенных людей и заработанную сумму",
                           reply_markup=keyboard,
                           disable_web_page_preview=True)


async def admin_cabinet(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    but1 = types.InlineKeyboardButton(text="Узнать баланс бота", callback_data="get_balance")
    but2 = types.InlineKeyboardButton(text="Пополнить баланс бота", callback_data="add_balance")
    but3 = types.InlineKeyboardButton(text="Топ рефералов", callback_data="top_lider")
    but4 = types.InlineKeyboardButton(text="Добавить уникальный баланс",
                                      callback_data="unik_user")
    but5 = types.InlineKeyboardButton(text="Перейти в режим юзера", callback_data="rej_user")
    keyboard.add(but1, but2, but3, but4, but5)

    famous = await big_og()
    await bot.send_message(chat_id=message.chat.id,
                           text=f"<b>Добро пожаловать в админ панель! 🧑🏼‍💻</b>\n\n"
                                f"<b>🥸 Людей в базе:</b> {base.get_count_man()} человек\n"
                                f"<b>🏆 Самый крутой:</b> @{famous}",
                           reply_markup=keyboard,
                           disable_web_page_preview=True)


#### ALL INLINE MODE ####
@dp.callback_query_handler(state="*")
async def inline_kb_answer_callback_handler(query: types.CallbackQuery, state: FSMContext):
    if (query.data == "start"):
        keyboard = types.InlineKeyboardMarkup()
        but1 = types.InlineKeyboardButton(text="Я выполнил все условия", callback_data="check")
        keyboard.add(but1)

        await bot.send_chat_action(chat_id=query.message.chat.id,
                                   action="typing")
        await bot.edit_message_text(chat_id=query.message.chat.id,
                                    message_id=query.message.message_id,
                                    text="<b>Подписывайся на наш канал “Русяев и партнёры”</b> - @in_rusyaev.\n\n"
                                         "<b>1)</b> Поставь лайк на крайний пост\n"
                                         "<b>2)</b> Прокомментируй любой пост, предварительно прочитав его\n\n"
                                         "<i><b>Комментарии, содержащие только смайлик или одно слово, проверку не пройдут</b></i>\n\n"
                                         "<i>После того, как выполнишь все условия, возвращайся в бот и нажми кнопку <b>“Я выполнил все условия”</b></i>",
                                    reply_markup=keyboard)

    elif (query.data == "second_check"):
        if (await in_chat(query.message)) == True:
            await bot.edit_message_text(chat_id=query.message.chat.id,
                                        message_id=query.message.message_id,
                                        text="Хорошо, вы снова на проверке. Ожидайте зачисления")
            await sleep_wait(query.message)

        elif (await in_chat(query.message)) != True:
            keyboard = types.InlineKeyboardMarkup()
            but1 = types.InlineKeyboardButton(text="Проверить еще раз", callback_data="second_check")
            keyboard.add(but1)

            await bot.edit_message_text(chat_id=query.message.chat.id,
                                        message_id=query.message.message_id,
                                        text="Вы не подписаны на канал",
                                        reply_markup=keyboard)

    elif (query.data == "check"):
        if (await in_chat(query.message) == True): # check sub
            try:
                if (await check_message(query.message.chat.id) == True): # check message
                    keyboard = types.InlineKeyboardMarkup()
                    but1 = types.InlineKeyboardButton(text="Пройти каптчу", callback_data="captcha")
                    keyboard.add(but1)

                    await bot.edit_message_text(chat_id=query.message.chat.id,
                                                message_id=query.message.message_id,
                                                text="<b>🤖 Хорошо, все условия выполнены!</b>\n\n"
                                                     "<i>Осталось только проверить, что вы не робот</i>",
                                                reply_markup=keyboard)

                elif (await check_message(query.message.chat.id) == False):
                    keyboard = types.InlineKeyboardMarkup()
                    but1 = types.InlineKeyboardButton(text="Я оставил комменатрий", callback_data="check")
                    keyboard.add(but1)

                    await bot.answer_callback_query(callback_query_id=query.id, text='⚠️ Комментарий не оставлен!',
                                                    show_alert=True)
                    await bot.edit_message_text(chat_id=query.message.chat.id,
                                                message_id=query.message.message_id,
                                                text="<b>Вы забыли оставить комментарий @in_rusyaev</b>\n\n"
                                                     "<i>Я подожду</i> 🤨",
                                                reply_markup=keyboard,
                                                disable_web_page_preview=True)

            except Exception:
                pass
        else:
            try:
                keyboard = types.InlineKeyboardMarkup()
                but1 = types.InlineKeyboardButton(text="Я выполнил все условия", callback_data="check")
                keyboard.add(but1)

                await bot.answer_callback_query(callback_query_id=query.id, text='⚠️ Вы не подписаны!',
                                                show_alert=True)
                await bot.edit_message_text(chat_id=query.message.chat.id,
                                            message_id=query.message.message_id,
                                            text="<b>Вы забыли подписаться на канал @in_rusyaev!</b>\n\n"
                                                 "<i>Исправьте это</i> 😥",
                                            reply_markup=keyboard,
                                            disable_web_page_preview=True)
            except Exception:
                pass

    elif (query.data == "cabinet") or (query.data == "back"):
        keyboard = types.InlineKeyboardMarkup()
        but1 = types.InlineKeyboardButton(text="📈 Статистика", callback_data="stat")
        but2 = types.InlineKeyboardButton(text="🔗 Реферальная ссылка", callback_data="ref_link")
        but3 = types.InlineKeyboardButton(text="ℹ️ Правила", callback_data="rule")
        but4 = types.InlineKeyboardButton(text="💸 Запросить вывод", callback_data="money")
        keyboard.add(but2)
        keyboard.add(but1, but3)
        keyboard.add(but4)

        await bot.edit_message_text(chat_id=query.message.chat.id,
                                    message_id=query.message.message_id,
                                    text=f"<b>Это твой кабинет</b>\n\n"
                                         f"Здесь ты можешь получить реферальную ссылку, изучить правила, проверить количество приглашенных людей и заработанную сумму",
                                    reply_markup=keyboard,
                                    disable_web_page_preview=True)

    elif (query.data == "ref_link"):
        keyboard = types.InlineKeyboardMarkup()
        but1 = types.InlineKeyboardButton(text="📈 Статистика", callback_data="stat")
        but3 = types.InlineKeyboardButton(text="ℹ️ Правила", callback_data="rule")
        but4 = types.InlineKeyboardButton(text="💸 Запросить вывод", callback_data="money")
        keyboard.add(but1, but3)
        keyboard.add(but4)

        await bot.edit_message_text(chat_id=query.message.chat.id,
                                    message_id=query.message.message_id,
                                    text=f"<b>Это твой кабинет</b>\n\n"
                                         f"Здесь ты можешь получить реферальну ссылку, изучить правила, проверить количество приглашенных людей и заработанную сумму\n\n"
                                         f"<b>Реферальная ссылка:</b> <code>{await generate_ref(query.message)}</code>",
                                    reply_markup=keyboard,
                                    disable_web_page_preview=True)

    elif (query.data == "stat"):
        keyboard = types.InlineKeyboardMarkup()
        but1 = types.InlineKeyboardButton(text="⬅️ Вернуться", callback_data="back")
        keyboard.add(but1)

        await bot.edit_message_text(chat_id=query.message.chat.id,
                                    message_id=query.message.message_id,
                                    text=f"👤 Количество рефералов: {base.get_referal(query.message.chat.id)}\n"
                                         f"💵 Сумма заработка: {base.get_balance(query.message.chat.id)}\n\n"
                                         f"Текущий баланс: {base.get_withdraw(query.message.chat.id)}",
                                    reply_markup=keyboard,
                                    disable_web_page_preview=True)

    elif (query.data == "rule"):
        keyboard = types.InlineKeyboardMarkup()
        but1 = types.InlineKeyboardButton(text="⬅️ Вернуться", callback_data="back")
        keyboard.add(but1)

        await bot.edit_message_text(chat_id=query.message.chat.id,
                                    message_id=query.message.message_id,
                                    text="<b>💡 Правила и реферальная система</b>\n\n"
                                         "► <i>Чем больше вы приглашаете людей, тем больше ваш заработок!</i>\n"
                                         "► <i>Минимальный вывод от 0.16 $TON</i>\n"
                                         "► <i>Быстрое зачисление через <a href='t.me/CryptoBot?start=r-633430'>@CryptoBot</a></i>\n\n"
                                         "<code>10 человек - 0.015 $TON\n"
                                         "20 человек - 0.03 $TON\n"
                                         "30 человек - 0.048 $TON\n"
                                         "40 человек - 0.063 $TON\n"
                                         "50 человек - 0.079 $TON\n"
                                         "60 человек - 0.094 $TON\n"
                                         "70 человек - 0.11 $TON\n"
                                         "80 человек - 0.13 $TON\n"
                                         "90 человек - 0.14 $TON\n"
                                         "от 100 человек - 0.16 $TON</code>\n\n"
                                         "<b>Чем больше друзей, тем выше и ценнее награда</b>",
                                    reply_markup=keyboard,
                                    disable_web_page_preview=True)

    elif (query.data == "money"):
        keyboard = types.InlineKeyboardMarkup()
        but1 = types.InlineKeyboardButton(text="⬅️ Вернуться", callback_data="back")
        keyboard.add(but1)

        if (base.get_withdraw(query.message.chat.id) > 0):
            await bot.edit_message_text(chat_id=query.message.chat.id,
                                        message_id=query.message.message_id,
                                        text=f"На вывод {base.get_withdraw(query.message.chat.id)} $TON, заявка отправлена в очередь",
                                        reply_markup=keyboard,
                                        disable_web_page_preview=True)

            await referal_widthward(query.message)

        elif (base.get_withdraw(query.message.chat.id) == 0):
            await bot.edit_message_text(chat_id=query.message.chat.id,
                                        message_id=query.message.message_id,
                                        text="<b>У вас нулевой баланс!</b>",
                                        reply_markup=keyboard,
                                        disable_web_page_preview=True)

            # text = f"<b>На балансе недостаочно средств для вывода</b>\n\n"
            # f"Сумма сейчас {base.get_withdraw(query.message.chat.id)} $TON, не хватает {str(0.16 - base.get_withdraw(query.message.chat.id))[:4]} $TON",


    elif (query.data == "captcha"):
        await FSM_adv.first_captcha.set()
        code_captcha, photo_id = random.choice(list(config.captcha_list.items()))
        async with state.proxy() as forme:
            forme["code_captcha"] = code_captcha

        await bot.send_photo(chat_id=query.message.chat.id,
                             photo=photo_id)


    elif (query.data == "back_admin"):
        await state.finish()
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        but1 = types.InlineKeyboardButton(text="Узнать баланс бота", callback_data="get_balance")
        but2 = types.InlineKeyboardButton(text="Пополнить баланс бота", callback_data="add_balance")
        but3 = types.InlineKeyboardButton(text="Топ рефералов", callback_data="top_lider")
        but4 = types.InlineKeyboardButton(text="Добавить уникальный баланс", callback_data="unik_user")
        but5 = types.InlineKeyboardButton(text="Перейти в режим юзера", callback_data="rej_user")
        keyboard.add(but1, but2, but3, but4, but5)

        famous = await big_og()
        await bot.edit_message_text(chat_id=query.message.chat.id,
                                    message_id=query.message.message_id,
                                    text=f"<b>Добро пожаловать в админ панель! 🧑🏼‍💻</b>\n\n"
                                         f"<b>🥸 Людей в базе:</b> {base.get_count_man()} человек\n"
                                         f"<b>🏆 Самый крутой:</b> @{famous}",
                                    reply_markup=keyboard,
                                    disable_web_page_preview=True)

    elif (query.data == "get_balance"):
        try:
            keyboard = types.InlineKeyboardMarkup()
            but1 = types.InlineKeyboardButton(text="⬅️ Вернуться", callback_data="back_admin")
            keyboard.add(but1)

            answer_post = requests.post(url="https://pay.crypt.bot/api/getBalance",
                                        headers={"Host": "pay.crypt.bot",
                                                 "Crypto-Pay-API-Token": config.appl_token})

            need_json = answer_post.json()
            text = f"<b>💰 Счет бота:</b>\n\n" \
                   f"TON: {need_json['result'][1]['available']}\n" \
                   f"USDT {need_json['result'][5]['available']}\n" \

            await bot.edit_message_text(chat_id=query.message.chat.id,
                                        message_id=query.message.message_id,
                                        text=text,
                                        reply_markup=keyboard,
                                        disable_web_page_preview=True)

        except Exception as exep:
            await bot.edit_message_text(chat_id=query.message.chat.id,
                                        message_id=query.message.message_id,
                                        text=f"<b>Ошибка при запросе баланса</b>\n\n"
                                             f"<b>Код:</b> <code>{exep}</code>",
                                        reply_markup=keyboard,
                                        disable_web_page_preview=True)

    elif (query.data == "add_balance"):
        await FSM_adv.add_balance.set()
        keyboard = types.InlineKeyboardMarkup()
        but1 = types.InlineKeyboardButton(text="⬅️ Вернуться", callback_data="back_admin")
        keyboard.add(but1)

        await bot.edit_message_text(chat_id=query.message.chat.id,
                                    message_id=query.message.message_id,
                                    text="Отправьте сумму для пополнения\n\n"
                                         "Выбран TON",
                                    reply_markup=keyboard,
                                    disable_web_page_preview=True)

    elif (query.data == "top_lider"):
        keyboard = types.InlineKeyboardMarkup()
        but1 = types.InlineKeyboardButton(text="⬅️ Вернуться", callback_data="back_admin")
        keyboard.add(but1)

        list_lder = await liders_table()
        await bot.edit_message_text(chat_id=query.message.chat.id,
                                    message_id=query.message.message_id,
                                    text=list_lder,
                                    reply_markup=keyboard,
                                    disable_web_page_preview=True)

    elif (query.data == "unik_user"):
        await FSM_adv.add_unik_user.set()
        keyboard = types.InlineKeyboardMarkup()
        but1 = types.InlineKeyboardButton(text="⬅️ Вернуться", callback_data="back_admin")
        keyboard.add(but1)

        await bot.edit_message_text(chat_id=query.message.chat.id,
                                    message_id=query.message.message_id,
                                    text="<i>Отправьте ID человека</i>\n\n"
                                         "<b>Например:</b> <code>1095119526</code>",
                                    reply_markup=keyboard,
                                    disable_web_page_preview=True)

    elif (query.data == "rej_user"):
        await cabinet(query.message)


#### STATE HANDLERS ####
@dp.message_handler(state=FSM_adv.first_captcha)
async def answer_code(message: types.Message, state: FSMContext):
    data_list = await state.get_data()
    need_code = data_list["code_captcha"]

    if ((message.text).lower() == need_code.lower()):
        keyboard = types.InlineKeyboardMarkup()
        but1 = types.InlineKeyboardButton(text="Кабинет", callback_data="cabinet")
        keyboard.add(but1)

        await message.answer(text="<b>✅ Отлично!</b>\n\n"
                                  "Проверка действий займёт 24 часа, по истечении которых тебе придут токены TON на счет. Для зачисления вам нужно запустить <a href='t.me/CryptoBot?start=r-633430'>@CryptoBot</a> 👈\n\n"
                                  "👥 <i>Приглашай своих друзей в этот бот по своей реферальной ссылке и за каждого приведенного друга, получайте еще TON!</i>\n\n",
                            reply_markup=keyboard,
                             disable_web_page_preview=True)
        await state.finish()
        await sleep_wait(message)

    else:
        await message.reply(text="<b>❌ Неверный ввод, попробуйте еще раз</b>")
        code_captcha, photo_id = random.choice(list(config.captcha_list.items()))
        async with state.proxy() as forme:
            forme["code_captcha"] = code_captcha

        await bot.send_photo(chat_id=message.chat.id,
                             photo=photo_id)


if __name__ == '__main__':
    print("Bot work")
    executor.start_polling(dp)
