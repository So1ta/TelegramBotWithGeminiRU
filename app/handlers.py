from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from config import AI_TOKEN
from app.states import AI

import google.generativeai as genai

router = Router()

genai.configure(api_key=AI_TOKEN)
model = genai.GenerativeModel('gemini-1.5-flash')

@router.message(CommandStart())
async def cmd_start(message: Message):
	await message.answer('Welcome')

@router.message(AI.answer)
async def answer(message: Message):
	await message.answer('Wait')

@router.message(F.text)
async def ai(message: Message, state: FSMContext):
	await state.set_state(AI.answer)
	try:
		chat = (await state.get_data())['context']
		if len(chat.history) > 10:
			chat = model.start_chat(history=[])
		response = await chat.send_message_async(message.text)
		await state.update_data(context=chat)
	except:
		chat = model.start_chat(history=[])
		response = await chat.send_message_async(message.text)
		await state.update_data(context=chat)
	await message.answer(response.text)
	await state.clear()

