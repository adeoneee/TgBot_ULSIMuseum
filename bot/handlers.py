from aiogram import Dispatcher
from aiogram.types import Message, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup
from aiogram import filters
from aiogram import Bot
from db.db_connection import save_submission_to_db  
 
class SubmissionForm(StatesGroup):
    full_name = State()
    age = State()
    workplace = State()
    contacts = State()
    description = State()
    file = State()

async def start_command(message: Message):
    await message.answer("Добро пожаловать! Я бот для сбора заявок. Используйте /submit для подачи заявки.")
 
async def submit_command(message: Message, state: FSMContext):
    await message.answer("Введите ваше ФИО:")
    await state.set_state(SubmissionForm.full_name)   
 
async def process_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("Введите ваш возраст:")
    await state.set_state(SubmissionForm.age)   

async def process_age(message: Message, state: FSMContext):
    if not message.text.isdigit() or int(message.text) <= 0:
        await message.answer("Пожалуйста, введите корректный возраст (число).")
        return
    await state.update_data(age=int(message.text))
    await message.answer("Укажите место работы или учёбы:")
    await state.set_state(SubmissionForm.workplace)   

async def process_workplace(message: Message, state: FSMContext):
    await state.update_data(workplace=message.text)
    await message.answer("Введите ваши контактные данные (телефон, email):")
    await state.set_state(SubmissionForm.contacts)   

async def process_contacts(message: Message, state: FSMContext):
    await state.update_data(contacts=message.text)
    await message.answer("Кратко опишите вашу работу:")
    await state.set_state(SubmissionForm.description)   

async def process_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Загрузите ZIP-файл с вашей работой:")
    await state.set_state(SubmissionForm.file)  

async def process_file(message: Message, state: FSMContext, bot: Bot):
    if message.content_type != ContentType.DOCUMENT:
        await message.answer("Пожалуйста, загрузите файл формата ZIP.")
        return

    file = message.document
    if not file.file_name.endswith(".zip"):
        await message.answer("Пожалуйста, загрузите файл с расширением .zip.")
        return

    file_info = await bot.get_file(file.file_id)

    file_path = f"uploads/{file.file_name}"

    await bot.download_file(file_info.file_path, destination=file_path)

    data = await state.get_data()
    data["file_path"] = file_path

    username = message.from_user.username if message.from_user.username else "Не указан"
    data["username"] = username
    
    await save_submission_to_db(data)
    
    await message.answer("Ваша заявка успешно подана! Спасибо за участие.")
    await state.clear() 
 
def register_handlers(dp: Dispatcher):
    dp.message.register(submit_command, filters.Command("submit"))
    dp.message.register(process_full_name, filters.StateFilter(SubmissionForm.full_name))
    dp.message.register(process_age, filters.StateFilter(SubmissionForm.age))
    dp.message.register(process_workplace, filters.StateFilter(SubmissionForm.workplace))
    dp.message.register(process_contacts, filters.StateFilter(SubmissionForm.contacts))
    dp.message.register(process_description, filters.StateFilter(SubmissionForm.description))
    dp.message.register(process_file, filters.StateFilter(SubmissionForm.file))
    dp.message.register(start_command, filters.Command("start"))
