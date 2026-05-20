"""
🕵️ Spyfall Bot — игра «Шпион» на тему Brawl Stars
Использует aiogram 3.x + FSM (MemoryStorage)

Установка зависимостей:
    pip install aiogram==3.x

Запуск:
    python spyfall_bot.py

Замените BOT_TOKEN своим токеном от @BotFather.
"""

import asyncio
import random
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# ──────────────────────────────────────────────
# НАСТРОЙКИ
# ──────────────────────────────────────────────
BOT_TOKEN = "8958624774:AAE8osKzUPF7VHXpEE50pnUYehXMfh56Lco"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# ДАННЫЕ ТЕМЫ "BRAWL STARS"
# ──────────────────────────────────────────────
BRAWL_STARS_FIGHTERS = [
    {"name": "Шелли",         "role": "Урон"},
    {"name": "Нита",           "role": "Урон"},
    {"name": "Кольт",          "role": "Урон"},
    {"name": "Булл",           "role": "Танк"},
    {"name": "Брок",           "role": "Стрелок"},
    {"name": "Барли",          "role": "Артиллерия"},
    {"name": "Эль Примо",      "role": "Танк"},
    {"name": "Поко",           "role": "Поддержка"},
    {"name": "Роза",           "role": "Танк"},
    {"name": "Джесси",         "role": "Контроль"},
    {"name": "Динамайк",       "role": "Артиллерия"},
    {"name": "Рико",           "role": "Урон"},
    {"name": "Дэррил",         "role": "Танк"},
    {"name": "Пенни",          "role": "Артиллерия"},
    {"name": "Карл",           "role": "Урон"},
    {"name": "Джеки",          "role": "Танк"},
    {"name": "Гас",            "role": "Поддержка"},
    {"name": "Тик",            "role": "Артиллерия"},
    {"name": "8-Бит",          "role": "Урон"},
    {"name": "Бо",             "role": "Контроль"},
    {"name": "Пайпер",         "role": "Стрелок"},
    {"name": "Пэм",            "role": "Поддержка"},
    {"name": "Фрэнк",          "role": "Танк"},
    {"name": "Биби",           "role": "Танк"},
    {"name": "Беа",            "role": "Стрелок"},
    {"name": "Эмз",            "role": "Контроль"},
    {"name": "Гейл",           "role": "Контроль"},
    {"name": "Нани",           "role": "Стрелок"},
    {"name": "Колетт",         "role": "Урон"},
    {"name": "Эдгар",          "role": "Убийца"},
    {"name": "Сту",            "role": "Убийца"},
    {"name": "Белль",          "role": "Стрелок"},
    {"name": "Гром",           "role": "Артиллерия"},
    {"name": "Грифф",          "role": "Контроль (самый лучший боец)"},
    {"name": "Эш",             "role": "Танк"},
    {"name": "Лола",           "role": "Урон"},
    {"name": "Бонни",          "role": "Стрелок"},
    {"name": "Сэм",            "role": "Убийца"},
    {"name": "Мэнди",          "role": "Стрелок"},
    {"name": "Мэйси",          "role": "Стрелок"},
    {"name": "Хэнк",           "role": "Танк"},
    {"name": "Перл",           "role": "Урон"},
    {"name": "Ларри и Лори",   "role": "Артиллерия"},
    {"name": "Анджело",        "role": "Стрелок"},
    {"name": "Берри",          "role": "Поддержка"},
    {"name": "Шейд",           "role": "Убийца"},
    {"name": "Мипл",           "role": "Контроль"},
    {"name": "Транк",          "role": "Танк"},
    {"name": "Мортис",         "role": "Убийца"},
    {"name": "Тара",           "role": "Урон"},
    {"name": "Джин",           "role": "Контроль"},
    {"name": "Мистер П",       "role": "Контроль"},
    {"name": "Макс",           "role": "Поддержка"},
    {"name": "Спраут",         "role": "Артиллерия"},
    {"name": "Лу",             "role": "Контроль"},
    {"name": "Байрон",         "role": "Поддержка"},
    {"name": "Генерал Гавс",   "role": "Поддержка"},
    {"name": "Сквик",          "role": "Контроль"},
    {"name": "Базз",           "role": "Убийца"},
    {"name": "Фэнг",           "role": "Убийца"},
    {"name": "Ева",            "role": "Урон"},
    {"name": "Джанет",         "role": "Стрелок"},
    {"name": "Отис",           "role": "Контроль"},
    {"name": "Бастер",         "role": "Танк"},
    {"name": "Грей",           "role": "Поддержка"},
    {"name": "R-T",            "role": "Урон"},
    {"name": "Виллоу",         "role": "Контроль"},
    {"name": "Даг",            "role": "Поддержка"},
    {"name": "Чак",            "role": "Контроль"},
    {"name": "Чарли",          "role": "Контроль"},
    {"name": "Мико",           "role": "Убийца"},
    {"name": "Мелоди",         "role": "Убийца"},
    {"name": "Лили",           "role": "Убийца"},
    {"name": "Клэнси",         "role": "Урон"},
    {"name": "Мо",             "role": "Урон"},
    {"name": "Джуджу",         "role": "Артиллерия"},
    {"name": "Олли",           "role": "Танк"},
    {"name": "Луми",           "role": "Урон"},
    {"name": "Финкс",          "role": "Контроль"},
    {"name": "Джэ-Ён",         "role": "Поддержка"},
    {"name": "Алли",           "role": "Убийца"},
    {"name": "Мина",           "role": "Урон"},
    {"name": "Зигги",          "role": "Контроль"},
    {"name": "ДжиДжи",         "role": "Убийца"},
    {"name": "Глоуи",          "role": "Поддержка"},
    {"name": "Наджия",         "role": "Урон"},
    {"name": "Спайк",          "role": "Урон"},
    {"name": "Ворон",          "role": "Убийца"},
    {"name": "Леон",           "role": "Убийца"},
    {"name": "Сэнди",          "role": "Контроль"},
    {"name": "Вольт",          "role": "Урон"},
    {"name": "Амбер",          "role": "Контроль"},
    {"name": "Мэг",            "role": "Танк"},
    {"name": "Честер",         "role": "Урон"},
    {"name": "Корделиус",      "role": "Убийца"},
    {"name": "Кит",            "role": "Поддержка"},
    {"name": "Драко",          "role": "Танк"},
    {"name": "Кэндзи",         "role": "Убийца"},
    {"name": "Пирс",           "role": "Стрелок"},
    {"name": "Кадзэ",          "role": "Убийца"},
    {"name": "Сириус",         "role": "Контроль"},
    {"name": "Дамиан",         "role": "Танк"},
]

# ──────────────────────────────────────────────
# FSM СОСТОЯНИЯ
# ──────────────────────────────────────────────
class GameStates(StatesGroup):
    choosing_theme    = State()
    entering_players  = State()
    entering_spies    = State()
    showing_roles     = State()
    game_started      = State()


# ──────────────────────────────────────────────
# КЛАВИАТУРЫ
# ──────────────────────────────────────────────
def kb_start() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Старт", callback_data="start_game")]
    ])

def kb_themes() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚔️ Brawl Stars", callback_data="theme_brawlstars")]
    ])

def kb_show_role() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👁 Показать роль", callback_data="show_role")]
    ])

def kb_hide_role() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🙈 Скрыть роль", callback_data="hide_role")]
    ])

def kb_game_ended() -> InlineKeyboardMarkup:
    """Кнопки по окончании раздачи ролей — показать роли и играть снова."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Показать все роли", callback_data="show_all_roles")],
        [InlineKeyboardButton(text="🔁 Играть снова", callback_data="play_again")],
    ])


# ──────────────────────────────────────────────
# ГЕНЕРАЦИЯ РОЛЕЙ
# ──────────────────────────────────────────────
def generate_roles(num_players: int, num_spies: int) -> list[dict]:
    fighter = random.choice(BRAWL_STARS_FIGHTERS)
    spy_indices = set(random.sample(range(num_players), num_spies)) if num_spies > 0 else set()
    roles = []
    for i in range(num_players):
        roles.append({
            "player": i + 1,
            "is_spy": i in spy_indices,
            "character": fighter["name"],
            "fighter_role": fighter["role"],
        })
    return roles


# ──────────────────────────────────────────────
# ХЭНДЛЕРЫ
# ──────────────────────────────────────────────
async def cmd_start(message: Message, state: FSMContext):
    """Команда /start — приветствие, сбрасываем всё включая сохранённые настройки."""
    await state.clear()
    await message.answer(
        "👋 Добро пожаловать в игру <b>«Шпион»</b>!\n\n"
        "Один из игроков окажется шпионом — он не знает свою роль. "
        "Остальные должны его вычислить!\n\n"
        "Нажмите кнопку ниже, чтобы начать.",
        reply_markup=kb_start(),
        parse_mode="HTML",
    )


async def cmd_help(message: Message):
    """Команда /help — справка."""
    await message.answer(
        "📖 <b>Команды бота:</b>\n\n"
        "/start — начать новую игру\n"
        "/newgame — начать новую игру заново\n"
        "/help — показать это сообщение\n\n"
        "<b>Как играть:</b>\n"
        "1. Выберите тему\n"
        "2. Введите количество игроков (3–12)\n"
        "3. Введите количество шпионов (0–12)\n"
        "4. Каждый игрок по очереди смотрит свою роль\n"
        "5. Мирные знают бойца, шпион знает только его класс\n"
        "6. Обсуждайте и вычисляйте шпиона!",
        parse_mode="HTML",
    )


async def cmd_newgame(message: Message, state: FSMContext):
    """Команда /newgame — сбросить и начать заново."""
    await state.clear()
    await message.answer(
        "🔄 Игра сброшена! Начинаем заново.\n\n"
        "Нажмите кнопку ниже, чтобы начать.",
        reply_markup=kb_start(),
        parse_mode="HTML",
    )


async def cb_start_game(callback: CallbackQuery, state: FSMContext):
    """Нажата кнопка «Старт»."""
    await state.set_state(GameStates.choosing_theme)
    await callback.message.edit_text(
        "🎯 <b>Выберите тему игры:</b>",
        reply_markup=kb_themes(),
        parse_mode="HTML",
    )
    await callback.answer()


async def cb_choose_theme(callback: CallbackQuery, state: FSMContext):
    """Выбрана тема — сохраняем message_id чтобы потом удалить запрос игроков."""
    await state.update_data(theme="brawlstars")
    await state.set_state(GameStates.entering_players)
    # Редактируем сообщение и сохраняем его id для последующего удаления
    msg = await callback.message.edit_text(
        "👥 <b>Введите количество игроков</b> (от 3 до 12):",
        parse_mode="HTML",
    )
    await state.update_data(ask_players_msg_id=msg.message_id)
    await callback.answer()


async def msg_enter_players(message: Message, state: FSMContext):
    """Ввод количества игроков."""
    data = await state.get_data()
    text = message.text.strip()

    # Удаляем сообщение пользователя с числом
    try:
        await message.delete()
    except Exception:
        pass

    if not text.isdigit():
        await message.answer("⚠️ Пожалуйста, введите <b>целое число</b>.", parse_mode="HTML")
        return

    num = int(text)
    if not (3 <= num <= 12):
        await message.answer("⚠️ Количество игроков должно быть от <b>3</b> до <b>12</b>.", parse_mode="HTML")
        return

    # Удаляем сообщение бота «Введите количество игроков»
    try:
        await message.bot.delete_message(message.chat.id, data["ask_players_msg_id"])
    except Exception:
        pass

    await state.update_data(num_players=num)
    await state.set_state(GameStates.entering_spies)

    # Отправляем запрос шпионов и сохраняем его id
    msg = await message.answer(
        f"🕵️ <b>Введите количество шпионов</b> (от 0 до 12):",
        parse_mode="HTML",
    )
    await state.update_data(ask_spies_msg_id=msg.message_id)


async def msg_enter_spies(message: Message, state: FSMContext):
    """Ввод количества шпионов."""
    data = await state.get_data()
    num_players = data["num_players"]
    text = message.text.strip()

    # Удаляем сообщение пользователя с числом
    try:
        await message.delete()
    except Exception:
        pass

    if not text.isdigit():
        await message.answer("⚠️ Пожалуйста, введите <b>целое число</b>.", parse_mode="HTML")
        return

    num_spies = int(text)

    if num_spies < 0:
        await message.answer("⚠️ Количество шпионов не может быть отрицательным.", parse_mode="HTML")
        return
    if num_spies > num_players:
        await message.answer(
            f"⚠️ Шпионов не может быть больше, чем игроков ({num_players}).",
            parse_mode="HTML",
        )
        return

    # Удаляем сообщение бота «Введите количество шпионов»
    try:
        await message.bot.delete_message(message.chat.id, data["ask_spies_msg_id"])
    except Exception:
        pass

    roles = generate_roles(num_players, num_spies)

    await state.update_data(
        num_spies=num_spies,
        roles=roles,
        current_player_index=0,
    )
    await state.set_state(GameStates.showing_roles)

    # Сразу показываем первого игрока — без строки «✅ Шпионов: N»
    await message.answer(
        "🎲 Роли распределены! Начинаем раздачу.\n\n"
        "📱 <b>Игрок 1</b>, узнай свою роль.",
        reply_markup=kb_show_role(),
        parse_mode="HTML",
    )


async def cb_show_role(callback: CallbackQuery, state: FSMContext):
    """Показать роль игрока."""
    data = await state.get_data()
    roles = data["roles"]
    idx = data["current_player_index"]
    role = roles[idx]

    if role["is_spy"]:
        role_text = (
            "🕵️ <b>Вы — ШПИОН!</b>\n\n"
            f"🎭 Подсказка — класс бойца: <b>{role['fighter_role']}</b>\n\n"
            "Вы не знаете, кто именно этот боец.\n"
            "Старайтесь не раскрыть себя и вычислить его по разговору других!"
        )
    else:
        role_text = (
            f"✅ <b>Вы — мирный житель.</b>\n\n"
            f"🎮 Ваш боец: <b>{role['character']}</b>\n\n"
            "Никому не раскрывайте это!"
        )

    await callback.message.edit_text(
        role_text,
        reply_markup=kb_hide_role(),
        parse_mode="HTML",
    )
    await callback.answer()


async def cb_hide_role(callback: CallbackQuery, state: FSMContext):
    """Скрыть роль и перейти к следующему игроку."""
    data = await state.get_data()
    roles = data["roles"]
    idx = data["current_player_index"]
    next_idx = idx + 1

    if next_idx < len(roles):
        await state.update_data(current_player_index=next_idx)
        await callback.message.edit_text(
            f"📱 <b>Игрок {next_idx + 1}</b>, подойди к экрану.",
            reply_markup=kb_show_role(),
            parse_mode="HTML",
        )
    else:
        await state.set_state(GameStates.game_started)
        await callback.message.edit_text(
            "🎉 <b>Все игроки узнали свои роли.</b>\n\n"
            "🚀 <b>Игра началась!</b> Включите таймер.\n\n"
            "Задавайте вопросы по кругу. Шпион должен остаться неразоблачённым!",
            reply_markup=kb_game_ended(),
            parse_mode="HTML",
        )

    await callback.answer()


async def cb_show_all_roles(callback: CallbackQuery, state: FSMContext):
    """Показать все роли после игры."""
    data = await state.get_data()
    roles = data.get("roles", [])

    if not roles:
        await callback.answer("Нет данных об игре.", show_alert=True)
        return

    lines = ["📋 <b>Итоги игры — роли игроков:</b>\n"]
    for role in roles:
        if role["is_spy"]:
            lines.append(f"🕵️ Игрок {role['player']} — <b>ШПИОН</b> (подсказка: {role['fighter_role']})")
        else:
            lines.append(f"✅ Игрок {role['player']} — <b>{role['character']}</b>")

    await callback.message.answer("\n".join(lines), parse_mode="HTML")
    await callback.answer()


async def cb_play_again(callback: CallbackQuery, state: FSMContext):
    """Играть снова — сохраняем кол-во игроков и шпионов, просто перераздаём роли."""
    data = await state.get_data()
    num_players = data.get("num_players")
    num_spies = data.get("num_spies")

    # Генерируем новые роли с теми же настройками
    roles = generate_roles(num_players, num_spies)

    await state.update_data(
        roles=roles,
        current_player_index=0,
    )
    await state.set_state(GameStates.showing_roles)

    await callback.message.edit_text(
        f"🔁 <b>Новый раунд!</b>\n"
        f"👥 Игроков: <b>{num_players}</b> | 🕵️ Шпионов: <b>{num_spies}</b>\n\n"
        "🎲 Роли перераспределены!\n\n"
        "📱 <b>Игрок 1</b>, узнай свою роль.",
        reply_markup=kb_show_role(),
        parse_mode="HTML",
    )
    await callback.answer()


# ──────────────────────────────────────────────
# УСТАНОВКА КОМАНД В МЕНЮ TELEGRAM
# ──────────────────────────────────────────────
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start",   description="🎮 Начать игру"),
        BotCommand(command="newgame", description="🔄 Новая игра"),
        BotCommand(command="help",    description="📖 Помощь"),
    ]
    await bot.set_my_commands(commands)


# ──────────────────────────────────────────────
# ТОЧКА ВХОДА
# ──────────────────────────────────────────────
async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрируем хэндлеры
    dp.message.register(cmd_start,          CommandStart())
    dp.message.register(cmd_help,           Command("help"))
    dp.message.register(cmd_newgame,        Command("newgame"))
    dp.message.register(msg_enter_players,  GameStates.entering_players)
    dp.message.register(msg_enter_spies,    GameStates.entering_spies)

    dp.callback_query.register(cb_start_game,     F.data == "start_game")
    dp.callback_query.register(cb_choose_theme,   F.data == "theme_brawlstars")
    dp.callback_query.register(cb_show_role,      F.data == "show_role",      GameStates.showing_roles)
    dp.callback_query.register(cb_hide_role,      F.data == "hide_role",      GameStates.showing_roles)
    dp.callback_query.register(cb_show_all_roles, F.data == "show_all_roles", GameStates.game_started)
    dp.callback_query.register(cb_play_again,     F.data == "play_again",     GameStates.game_started)

    # Устанавливаем команды в меню Telegram
    await set_commands(bot)

    logger.info("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
