from aiogram import Bot, F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, KeyboardButton, InlineKeyboardButton, CallbackQuery
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from config import ADMINS_LIST

rt = Router()

ADMINS = ADMINS_LIST


class FormStates(StatesGroup):
    head = State()
    status = State()
    fullname = State()
    age = State()
    tech = State()
    contact = State()
    region = State()
    price = State()
    job = State()
    time_contact = State()
    aim = State()
    last = State()


async def buttons(lang_code):
    rbk = ReplyKeyboardBuilder()
    rbk.add(KeyboardButton(text=_('Sherik kerak', locale=lang_code)))
    rbk.add(KeyboardButton(text=_('Ish joyi kerak', locale=lang_code)))
    rbk.add(KeyboardButton(text=_('Xodim kerak', locale=lang_code)))
    rbk.add(KeyboardButton(text=_('Ustoz kerak', locale=lang_code)))
    rbk.add(KeyboardButton(text=_('Shogird kerak', locale=lang_code)))
    rbk.adjust(2, 2, 1)
    return rbk.as_markup(resize_keyboard=True)


async def text_sample(data, message: Message):
    data_status = f"{data['status'][2:].lower()}"
    username = f'{message.from_user.username}'
    text = _("""{d1}:

{d2}: {d3}
🕑 Yosh: {d4}
📚 Texnologiya: {d5}
🇺🇿 Telegram: @{us}
📞 Aloqa: {d6}
🌐 Hudud: {d7}   
💰 Narxi: {d8}
👨🏻‍💻 Kasbi: {d9}
🕰 Murojaat qilish vaqti: {d10}
🔎 Maqsad: {d11}

#{d13}""").format(d1=data['head'], d2=data['status'], d3=data['fullname'], d4=data['age'],
                  d5=data['tech'], d6=data['contact'], d7=data['region'], d8=data['price'],
                  d9=data['job'], d10=data['time_contact'], d11=data['aim'], d13=data_status,
                  us=username)
    return text


@rt.message(CommandStart())
async def start(message: Message, state: FSMContext):
    rbk = InlineKeyboardBuilder()
    rbk.add(InlineKeyboardButton(text="RU🇷🇺", callback_data="lang_ru"))
    rbk.add(InlineKeyboardButton(text="UZ🇺🇿", callback_data="lang_uz"))
    await message.answer(_("Tilni tanlang: "), reply_markup=rbk.as_markup())


@rt.callback_query(F.data.startswith('lang_'))
async def start(callback: CallbackQuery, state: FSMContext):
    lang_code = callback.data.split('lang_')[-1]
    await state.update_data(locale=lang_code)
    fullname1 = callback.from_user.full_name
    text = _('Til tanlandi', locale=lang_code)
    await callback.answer(text)
    await callback.message.answer(_('''
    Assalom alaykum {fullname}
    UstozShogird kanalining rasmiy botiga xush kelibsiz!


    /help yordam buyrugi orqali nimalarga qodir ekanligimni bilib oling!''', locale=lang_code).format(
        fullname=fullname1), reply_markup=(await buttons(lang_code)))


@rt.message((F.text == __('Ish joyi kerak')) | (F.text == __('Xodim kerak')) | (F.text == __('Shogird kerak')) | (
        F.text == __('Ustoz kerak')) | (F.text == __('Sherik kerak')))
async def start(message: Message, state: FSMContext):
    await state.update_data(head=message.text)
    if message.text == _('Ish joyi kerak'):
        await state.update_data(status=_('👨‍💼 Xodim'))
    elif message.text == _('Xodim kerak'):
        await state.update_data(status=_('🏢 Idora'))
    elif message.text == _('Shogird kerak'):
        await state.update_data(status=_('🎓 Ustoz'))
    elif message.text == _('Ustoz kerak'):
        await state.update_data(status=_('🎓 Shogird'))
    elif message.text == _('Sherik kerak'):
        await state.update_data(status=_('🏅 Sherik'))
    await state.set_state(FormStates.fullname)
    if (await state.get_data())['locale'] == 'uz':
        head = f"{message.text.split(' kerak')[0]} topish uchun ariza berish"
    else:
        head = f'{message.text}'

    await message.answer(_("""
{headline}

Hozir sizga birnecha savollar beriladi. 
Har biriga javob bering. 
Oxirida agar hammasi to`g`ri bo`lsa, HA tugmasini bosing va arizangiz Adminga yuboriladi.""").format(headline=head))
    if (await state.get_data())['status'] == _('🏢 Idora'):
        await message.answer(_("Idora nomi?"))
    else:
        await message.answer(_("Ism, familiyangizni kiriting?"))


@rt.message(FormStates.fullname)
async def cmd_start(message: Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await state.set_state(FormStates.age)
    await message.answer(_("""
🕑 Yosh: 

Yoshingizni kiriting?
Masalan, 19"""))


@rt.message(FormStates.age)
async def cmd_start(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(FormStates.tech)
    await message.answer(_("""
📚 Texnologiya:

Talab qilinadigan texnologiyalarni kiriting?
Texnologiya nomlarini vergul bilan ajrating. Masalan, 

Java, C++, C#"""))


@rt.message(FormStates.tech)
async def cmd_start(message: Message, state: FSMContext):
    await state.update_data(tech=message.text)
    await state.set_state(FormStates.contact)
    await message.answer(_("""
📞 Aloqa: 

Bog`lanish uchun raqamingizni kiriting?
Masalan, +998 90 123 45 67"""))


@rt.message(FormStates.contact)
async def cmd_start(message: Message, state: FSMContext):
    await state.update_data(contact=message.text)
    await state.set_state(FormStates.region)
    await message.answer(_("""
🌐 Hudud: 

Qaysi hududdansiz?
Viloyat nomi, Toshkent shahar yoki Respublikani kiriting."""))


@rt.message(FormStates.contact)
async def cmd_start(message: Message, state: FSMContext):
    await state.update_data(contact=message.text)
    await state.set_state(FormStates.region)
    await message.answer("""
🌐 Hudud: 

Qaysi hududdansiz?
Viloyat nomi, Toshkent shahar yoki Respublikani kiriting.""")


@rt.message(FormStates.region)
async def cmd_start(message: Message, state: FSMContext):
    await state.update_data(region=message.text)
    await state.set_state(FormStates.price)
    await message.answer(_("""
💰 Narxi:

Tolov qilasizmi yoki Tekinmi?
Kerak bo`lsa, Summani kiriting?"""))


@rt.message(FormStates.price)
async def cmd_start(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(FormStates.job)
    await message.answer(_("""
👨🏻‍💻 Kasbi: 

Ishlaysizmi yoki o`qiysizmi?
Masalan, Talaba"""))


@rt.message(FormStates.job)
async def cmd_start(message: Message, state: FSMContext):
    await state.update_data(job=message.text)
    await state.set_state(FormStates.time_contact)
    await message.answer(_("""
🕰 Murojaat qilish vaqti: 

Qaysi vaqtda murojaat qilish mumkin?
Masalan, 9:00 - 18:00"""))


@rt.message(FormStates.time_contact)
async def cmd_start(message: Message, state: FSMContext):
    await state.update_data(time_contact=message.text)
    await state.set_state(FormStates.aim)
    await message.answer(_("""
🔎 Maqsad: 

Maqsadingizni qisqacha yozib bering."""))


@rt.message(FormStates.aim)
async def cmd_start(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(aim=message.text)
    await state.set_state(FormStates.aim)
    text = await text_sample(await state.get_data(), message)
    await message.answer(text)
    await state.set_state(FormStates.last)
    rbk = ReplyKeyboardBuilder()
    rbk.add(KeyboardButton(text=_('ha')))
    rbk.add(KeyboardButton(text=_('Yoq')))
    await message.answer(_("Barcha ma'lumotlar to'g'rimi?"), reply_markup=rbk.as_markup(resize_keyboard=True))


@rt.message(FormStates.last, F.text == __('ha'))
async def cmd_start(message: Message, state: FSMContext, bot: Bot):
    text = await text_sample(await state.get_data(), message)
    ikb = InlineKeyboardBuilder()
    ikb.add(InlineKeyboardButton(text=_('junatish'), callback_data=f'send_{message.message_id}'))
    await bot.send_message(ADMINS[0], text, reply_markup=ikb.as_markup())
    await state.set_state(FormStates.fullname)
    await state.clear()


@rt.message(FormStates.last, F.text == __('yoq'))
async def cmd_start(message: Message, state: FSMContext, bot: Bot):
    await state.clear()
    await state.set_state(FormStates.fullname)
