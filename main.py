from copy import deepcopy


from Bot import *
from DataBase import *


db_budget = DataBaseBudget('accounter.db')

# remember the current state
current_state = deepcopy(states["default"])


# processing the "/start" command
@bot.message_handler(commands=['start'])
def command_start(message):
    try:
        bot.send_message(message.chat.id, f"Добро пожаловать!", parse_mode='html')
        bot.send_message(
            message.chat.id,
            f"Здесь вы можете вести свой бюджет\n\n"
            f"<b>Доходы</b> вносятся в следующем формате:\n"
            f"&lt;сумма&gt;. &lt;источник дохода&gt;. &lt;банк&gt;. &lt;тип счета&gt;\n"
            f"Обязательным является параметр 'сумма', который является числом (целым или дробным)\n\n"
            f"<b>Расходы</b> вносятся в следующем формате:\n"
            f"&lt;сумма&gt; &lt;наименование&gt; &lt;категория&gt; &lt;количество&gt; &lt;масса&gt; &lt;кэшбэк&gt;\n"
            f"Обязательными являются параметры 'сумма', который является числом (целым или дробным), и 'наименование'\n\n"
            f"В настройках вы можете изменить значения разделителей между параметрами "
            f"(<b>sep</b> по умолчанию является точкой '<b>.</b>') "
            f"и между целой и дробной частями вводимых чисел "
            f"(<b>float_sep</b> по умолчанию является запятой '<b>,</b>')\n\n"
            f"Время используется московское",
            parse_mode='html'
        )
        bot.send_message(message.chat.id, f"Начнем!", parse_mode='html', reply_markup=states["default"]["markup"])
    except Exception as e:
        bot_error_stop(bot, message, bot_admin_id_telegram, e, db_budget)


# processing the "/help" command
@bot.message_handler(commands=['help'])
def command_help(message):
    try:
        bot.send_message(
            message.chat.id,
            f"Здесь вы можете вести свой бюджет\n\n"
            f"<b>Доходы</b> вносятся в следующем формате:\n"
            f"&lt;сумма&gt;. &lt;источник дохода&gt;. &lt;банк&gt;. &lt;тип счета&gt;\n"
            f"Обязательным является параметр 'сумма', который является числом (целым или дробным)\n\n"
            f"<b>Расходы</b> вносятся в следующем формате:\n"
            f"&lt;сумма&gt; &lt;наименование&gt; &lt;категория&gt; &lt;количество&gt; &lt;масса&gt; &lt;кэшбэк&gt;\n"
            f"Обязательными являются параметры 'сумма', который является числом (целым или дробным), и 'наименование'\n\n"
            f"В настройках вы можете изменить значения разделителей между параметрами "
            f"(<b>sep</b> по умолчанию является точкой '<b>.</b>') "
            f"и между целой и дробной частями вводимых чисел "
            f"(<b>float_sep</b> по умолчанию является запятой '<b>,</b>')\n\n"
            f"Время используется московское",
            parse_mode='html',
            reply_markup=states["default"]["markup"]
        )
    except Exception as e:
        bot_error_stop(bot, message, bot_admin_id_telegram, e, db_budget)


# processing user messages
@bot.message_handler(content_types=['text'])
def get_user_text(message):
    try:
        global current_state

        flag_update_state = False
        new_state = deepcopy(current_state)
        current_page = current_state["current_page"]

        if message.text == "Главное меню":
            # go to main menu
            flag_update_state = True
            new_state = deepcopy(states["default"])

        # If there were no changes, then check the command according to the bot structure
        if not flag_update_state:
            # update state
            if current_page == "Главное меню":
                flag_update_state = True

                if message.text == "Бюджет":
                    new_state = deepcopy(states["budget"])
                else:
                    flag_update_state = False

            elif current_page == "Бюджет":
                flag_update_state = True

                if message.text == "Добавить доходы":
                    new_state = deepcopy(states["add_revenue"])
                elif message.text == "Вывести доходы":
                    new_state = deepcopy(states["get_revenue"])
                elif message.text == "Добавить расходы":
                    new_state = deepcopy(states["add_expense"])
                elif message.text == "Вывести расходы":
                    new_state = deepcopy(states["get_expense"])
                elif message.text == "Настройки":
                    new_state = deepcopy(states["settings_budget"])
                elif message.text == "Назад":
                    # go to back
                    new_state = deepcopy(states["default"])
                else:
                    flag_update_state = False

            elif current_page == "Добавить доходы":
                flag_update_state = True

                if message.text == "Назад":
                    # go to back
                    new_state = deepcopy(states["budget"])
                else:
                    # message processing
                    # get users params
                    user_id = message.from_user.id
                    user_seps = db_budget.get_user_seps(user_id)
                    # divide the message into columns with 'sep'
                    columns = [i.strip() for i in str(message.text).split(user_seps[0])]

                    # message is correct? (first value is number)
                    if is_float_bot(columns[0], user_seps[1]):
                        if len(columns) < 5:
                            # add revenue to database
                            # make the number look like python float (sep='.') and convert to float
                            summa = float(columns[0].replace(user_seps[1], '.'))
                            # add a source of revenue, if available (columns[1])
                            source = None
                            if len(columns) >= 2:
                                source = columns[1]
                            # add a bank, if available (columns[2])
                            bank = None
                            if len(columns) >= 3:
                                bank = columns[2]
                            # add a account_type, if available (columns[3])
                            account_type = None
                            if len(columns) >= 4:
                                account_type = columns[3]

                            db_budget.add_revenue_record(user_id, summa, source, bank, account_type)
                            # send a success message
                            bot.send_message(
                                message.chat.id,
                                f"Запись о доходе успешно добавлена!",
                                parse_mode='html'
                            )
                        else:
                            # send an error message
                            bot.send_message(
                                message.chat.id,
                                f"Сообщение некорректно! Вы ввели слишком много параметров (должно быть 4 параметра). "
                                f"Возможно использованы неправильные резделители sep и float_sep",
                                parse_mode='html'
                            )
                    else:
                        # send an error message
                        bot.send_message(
                            message.chat.id,
                            f"Сообщение некорректно! Первый параметр должен быть суммой дохода. "
                            f"Возможно использованы неправильные резделители sep и float_sep",
                            parse_mode='html'
                        )
                    # update state
                    new_state = deepcopy(states["add_revenue"])

            elif current_page == "Вывести доходы":
                flag_update_state = True

                if message.text == "Назад":
                    # go to back
                    new_state = deepcopy(states["budget"])
                else:
                    # update state
                    new_state = deepcopy(states["get_revenue"])

                    # the user has selected a period
                    user_period = message.text
                    if user_period in bot_budget_user_periods:
                        # correct period
                        # determine the correct value of the period variable
                        period = db_budget_periods[bot_budget_user_periods.index(user_period)]
                        # get users params
                        user_id = message.from_user.id
                        user_seps = db_budget.get_user_seps(user_id)
                        # get users revenue
                        users_revenues = db_budget.get_revenue_records(user_id, period)
                        # message formation
                        bot_message = f"Доходы за {user_period}:"
                        main_summa = 0
                        for count, value in enumerate(users_revenues):
                            _, _, summa, source, bank, account_type, date = value
                            main_summa += float(summa)
                            # make the number look like user float (sep=user_seps[1])
                            summa = str(summa).replace('.', user_seps[1])
                            # processing None
                            if source       is None: source       = "None"
                            if bank         is None: bank         = "None"
                            if account_type is None: account_type = "None"
                            bot_message += f"\n{count + 1}). " + f"{user_seps[0]} ".join([summa, source, bank, account_type, date])

                        # make the number look like user float (sep=user_seps[1])
                        main_summa = str(main_summa).replace('.', user_seps[1])
                        bot_message += f"\n\nВсего было {len(users_revenues)} записей" \
                                       f"\nОбщая сумма: {main_summa} руб."

                        # send a message
                        bot.send_message(
                            message.chat.id,
                            bot_message,
                            parse_mode='html'
                        )
                    else:
                        # incorrect period. send an error message
                        bot.send_message(
                            message.chat.id,
                            f"Ошибка! Выберите период из предложенных!",
                            parse_mode='html'
                        )

            elif current_page == "Добавить расходы":
                flag_update_state = True

                if message.text == "Назад":
                    # go to back
                    new_state = deepcopy(states["budget"])
                else:
                    # message processing
                    # get users params
                    user_id = message.from_user.id
                    user_seps = db_budget.get_user_seps(user_id)
                    # divide the message into columns with 'sep'
                    columns = [i.strip() for i in str(message.text).split(user_seps[0])]

                    # message is correct?
                    # 0. the number of columns is less than 7
                    # 1. first value is number
                    # 2. there are second value
                    # 3. counter is a number, if available (columns[3])
                    # 4. mass is a number, if available (columns[4])
                    # 5. bonus is a number, if available (columns[5])
                    flag_message_correct = True
                    summa = 0
                    title = ""
                    category = None
                    counter = None
                    mass = None
                    bonus = None
                    # 0.
                    if len(columns) > 6:
                        flag_message_correct = False
                    # 1. and 2.
                    if len(columns) > 1:
                        if is_float_bot(columns[0], user_seps[1]):
                            # make the number look like python float (sep='.') and convert to float
                            summa = float(columns[0].replace(user_seps[1], '.'))
                            # add a title of expense
                            title = columns[1]
                        else:
                            flag_message_correct = False
                    else:
                        flag_message_correct = False
                    # category
                    if len(columns) > 2:
                        category = columns[2]
                    # 3.
                    if len(columns) > 3:
                        if is_float_bot(columns[3], user_seps[1]):
                            # make the number look like python float (sep='.') and convert to float
                            counter = float(columns[3].replace(user_seps[1], '.'))
                        else:
                            flag_message_correct = False
                    # 4.
                    if len(columns) > 4:
                        if is_float_bot(columns[4], user_seps[1]):
                            # make the number look like python float (sep='.') and convert to float
                            mass = float(columns[4].replace(user_seps[1], '.'))
                        else:
                            flag_message_correct = False
                    # 5.
                    if len(columns) > 5:
                        if is_float_bot(columns[5], user_seps[1]):
                            # make the number look like python float (sep='.') and convert to float
                            bonus = float(columns[5].replace(user_seps[1], '.'))
                        else:
                            flag_message_correct = False

                    if flag_message_correct:
                        # add expense to database
                        db_budget.add_expense_record(user_id, summa, title, category, counter, mass, bonus)
                        # send a success message
                        bot.send_message(
                            message.chat.id,
                            f"Запись о расходе успешно добавлена!",
                            parse_mode='html'
                        )
                    else:
                        # send an error message
                        bot.send_message(
                            message.chat.id,
                            f"Сообщение некорректно! Возможные ошибки:\n"
                            f"Использованы неправильные резделители sep и float_sep\n"
                            f"Должно быть не больше 6 параметров (первые 2 обязательные):\n"
                            f"1. Первый параметр - сумма расхода (число)\n"
                            f"2. Второй параметр - название расхода\n"
                            f"3. Третий параметр - категория расхода\n"
                            f"4. Четвертый паарметр - количество (число)\n"
                            f"5. Пятый параметр - масса (число)\n"
                            f"6. Четвертый паарметр - кэшбэк (число)",
                            parse_mode='html'
                        )
                    # update state
                    new_state = deepcopy(states["add_expense"])

            elif current_page == "Вывести расходы":
                flag_update_state = True

                if message.text == "Назад":
                    # go to back
                    new_state = deepcopy(states["budget"])
                else:
                    # update state
                    new_state = deepcopy(states["get_expense"])

                    # the user has selected a period
                    user_period = message.text
                    if user_period in bot_budget_user_periods:
                        # correct period
                        # determine the correct value of the period variable
                        period = db_budget_periods[bot_budget_user_periods.index(user_period)]
                        # get users params
                        user_id = message.from_user.id
                        user_seps = db_budget.get_user_seps(user_id)
                        # get users expenses
                        users_expenses = db_budget.get_expense_records(user_id, period)
                        # message formation
                        bot_message = f"Расходы за {user_period}:"
                        main_summa = 0
                        for count, value in enumerate(users_expenses):
                            _, _, summa, title, category, counter, mass, bonus, date = value
                            main_summa += float(summa)
                            # make the number look like user float (sep=user_seps[1])
                            summa = str(summa).replace('.', user_seps[1])
                            # processing None
                            category = "None" if category is None else str(category)
                            counter  = "None" if counter  is None else str(counter)
                            mass     = "None" if mass     is None else str(mass)
                            bonus    = "None" if bonus    is None else str(bonus)
                            bot_message += f"\n{count + 1}). " + f"{user_seps[0]} ".join(
                                [summa, title, category, counter, mass, bonus, date])

                        # make the number look like user float (sep=user_seps[1])
                        main_summa = str(main_summa).replace('.', user_seps[1])
                        bot_message += f"\n\nВсего было {len(users_expenses)} записей" \
                                       f"\nОбщая сумма: {main_summa} руб."

                        # send a message
                        bot.send_message(
                            message.chat.id,
                            bot_message,
                            parse_mode='html'
                        )
                    else:
                        # incorrect period. send an error message
                        bot.send_message(
                            message.chat.id,
                            f"Ошибка! Выберите период из предложенных!",
                            parse_mode='html'
                        )

            elif current_page == "Настройки Бюджет":
                flag_update_state = True

                if message.text == "sep":
                    # update state
                    new_state = deepcopy(states["settings_budget_sep"])
                elif message.text == "float_sep":
                    # update state
                    new_state = deepcopy(states["settings_budget_float_sep"])
                elif message.text == "Назад":
                    # go to back
                    new_state = deepcopy(states["budget"])
                else:
                    flag_update_state = False

            elif current_page == "sep Настройки Бюджет":
                flag_update_state = True

                if message.text == "Назад":
                    # go to back
                    new_state = deepcopy(states["settings_budget"])
                else:
                    # checking correctness
                    user_id = message.from_user.id
                    user_seps = db_budget.get_user_seps(user_id)
                    new_user_sep = message.text
                    if new_user_sep == user_seps[1]:
                        # send an error message
                        bot.send_message(
                            message.chat.id,
                            f"Написаный вами sep совпадает с float_sep! Выберите другой резделитель sep",
                            parse_mode='html'
                        )
                        # update state
                        new_state = deepcopy(states["settings_budget_sep"])
                    else:
                        # update "sep" and send a success message
                        db_budget.update_sep(user_id, new_user_sep)
                        bot.send_message(
                            message.chat.id,
                            f"Параметр sep успешно обновлен!",
                            parse_mode='html'
                        )
                        # update state
                        new_state = deepcopy(states["settings_budget"])

            elif current_page == "float_sep Настройки Бюджет":
                flag_update_state = True

                if message.text == "Назад":
                    # go to back
                    new_state = deepcopy(states["settings_budget"])
                else:
                    # checking correctness
                    user_id = message.from_user.id
                    user_seps = db_budget.get_user_seps(user_id)
                    new_user_float_sep = message.text
                    if new_user_float_sep == user_seps[0]:
                        # send an error message
                        bot.send_message(
                            message.chat.id,
                            f"Написаный вами float_sep совпадает с sep! Выберите другой резделитель float_sep",
                            parse_mode='html'
                        )
                        # update state
                        new_state = deepcopy(states["settings_budget_float_sep"])
                    else:
                        # update "float_sep" and send a success message
                        db_budget.update_float_sep(user_id, new_user_float_sep)
                        bot.send_message(
                            message.chat.id,
                            f"Параметр float_sep успешно обновлен!",
                            parse_mode='html'
                        )
                        # update state
                        new_state = deepcopy(states["settings_budget"])

            else:
                # go to main menu
                flag_update_state = True
                new_state = deepcopy(states["default"])

        # the state has not changed. send an error message
        if not flag_update_state:
            bot.send_message(message.chat.id, f"Нет такой команды!", parse_mode='html')

        # "bot_message" formation
        if new_state["current_page"] == "Настройки Бюджет":
            # get users 'sep' and 'float_sep'
            user_id = message.from_user.id
            user_seps = db_budget.get_user_seps(user_id)
            new_state["bot_message"] = f"Выберите что хотите изменить:" \
                                       f"\n'sep' = '{user_seps[0]}' (разделитель колонок)" \
                                       f"\n'float_sep' = '{user_seps[1]}' (разделитель целой и дробной частей числа)" \
                                       f"\n\nПример записи при текущих настройках:" \
                                       f"\n99{bot_float_sep}99{bot_sep} яблоки"

        # send a message
        bot.send_message(message.chat.id, new_state["bot_message"], parse_mode='html', reply_markup=new_state["markup"])
        # update current state
        current_state = deepcopy(new_state)
    except Exception as e:
        bot_error_stop(bot, message, bot_admin_id_telegram, e, db_budget)


bot.polling(none_stop=True)
