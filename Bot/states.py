from telebot import types


# state: default ("Главное меню")
markup_default = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton("Бюджет")
markup_default.add(btn1)

state_default = dict([
    ("markup", markup_default),
    ("bot_message", 'Выберите действие'),
    ("current_page", 'Главное меню')
])

# state: budget ("Бюджет")
markup_budget = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton("Добавить доходы")
btn2 = types.KeyboardButton("Добавить расходы")
btn3 = types.KeyboardButton("Вывести доходы")
btn4 = types.KeyboardButton("Вывести расходы")
btn5 = types.KeyboardButton("Настройки")
btn6 = types.KeyboardButton("Назад")
btn7 = types.KeyboardButton("Главное меню")
markup_budget.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)

state_budget = dict([
    ("markup", markup_budget),
    ("bot_message", "Выберите действие"),
    ("current_page", "Бюджет")
])

# state: add revenue ("Добавить доходы")
markup_add_revenue = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton("Назад")
btn2 = types.KeyboardButton("Главное меню")
markup_add_revenue.add(btn1, btn2)

state_add_revenue = dict([
    ("markup", markup_add_revenue),
    ("bot_message", "Введите доходы"),
    ("current_page", "Добавить доходы")
])

# state: add expense ("Добавить расходы")
markup_add_expense = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton("Назад")
btn2 = types.KeyboardButton("Главное меню")
markup_add_expense.add(btn1, btn2)

state_add_expense = dict([
    ("markup", markup_add_expense),
    ("bot_message", "Введите расходы"),
    ("current_page", "Добавить расходы")
])

# state: settings_budget ("Настройки" в "Бюджет")
markup_settings_budget = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton("sep")
btn2 = types.KeyboardButton("float_sep")
btn3 = types.KeyboardButton("Назад")
btn4 = types.KeyboardButton("Главное меню")
markup_settings_budget.add(btn1, btn2, btn3, btn4)

# "bot_message" is formed in the main program
state_settings_budget = dict([
    ("markup", markup_settings_budget),
    ("bot_message", "None"),
    ("current_page", "Настройки Бюджет")
])

# state: settings_budget_sep ("sep" в "Настройки" в "Бюджет")
markup_settings_budget_sep = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton("Назад")
btn2 = types.KeyboardButton("Главное меню")
markup_settings_budget_sep.add(btn1, btn2)

state_settings_budget_sep = dict([
    ("markup", markup_settings_budget_sep),
    ("bot_message", f"Введите новое значение параметра sep:"),
    ("current_page", "sep Настройки Бюджет")
])

# state: settings_budget_float_sep ("float_sep" в "Настройки" в "Бюджет")
markup_settings_budget_float_sep = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton("Назад")
btn2 = types.KeyboardButton("Главное меню")
markup_settings_budget_float_sep.add(btn1, btn2)

state_settings_budget_float_sep = dict([
    ("markup", markup_settings_budget_float_sep),
    ("bot_message", f"Введите новое значение параметра float_sep:"),
    ("current_page", "float_sep Настройки Бюджет")
])

# state: get_revenue  ("Вывести доходы")
markup_get_revenue = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton("День")
btn2 = types.KeyboardButton("Неделя")
btn3 = types.KeyboardButton("Месяц")
btn4 = types.KeyboardButton("Год")
btn5 = types.KeyboardButton("Весь период")
btn6 = types.KeyboardButton("Назад")
btn7 = types.KeyboardButton("Главное меню")
markup_get_revenue.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)

state_get_revenue = dict([
    ("markup", markup_get_revenue),
    ("bot_message", f"Выберите период, за который хотите увидеть доходы"),
    ("current_page", "Вывести доходы"),
])

# state: get_expense  ("Вывести расходы")
markup_get_expense = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton("День")
btn2 = types.KeyboardButton("Неделя")
btn3 = types.KeyboardButton("Месяц")
btn4 = types.KeyboardButton("Год")
btn5 = types.KeyboardButton("Весь период")
btn6 = types.KeyboardButton("Назад")
btn7 = types.KeyboardButton("Главное меню")
markup_get_expense.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)

state_get_expense = dict([
    ("markup", markup_get_expense),
    ("bot_message", f"Выберите период, за который хотите увидеть расходы"),
    ("current_page", "Вывести расходы"),
])

states = dict([
    ("default",                   state_default),
    ("budget",                    state_budget),
    ("add_revenue",               state_add_revenue),
    ("add_expense",               state_add_expense),
    ("settings_budget",           state_settings_budget),
    ("settings_budget_sep",       state_settings_budget_sep),
    ("settings_budget_float_sep", state_settings_budget_float_sep),
    ("get_revenue",               state_get_revenue),
    ("get_expense",               state_get_expense)
])
