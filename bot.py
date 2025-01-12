import streamlit as st
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests

# Initialize the Telegram bot
TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
bot = Bot(token=TELEGRAM_TOKEN)
updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Define the Hugging Face API endpoint
HUGGINGFACE_API_URL = 'https://api-inference.huggingface.co/models/YOUR_MODEL_NAME'
HUGGINGFACE_API_TOKEN = 'YOUR_HUGGINGFACE_API_TOKEN'

# Function to query Hugging Face space
def query_huggingface(text: str) -> str:
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}
    response = requests.post(HUGGINGFACE_API_URL, headers=headers, json={"inputs": text})
    return response.json()[0]['generated_text']

# Telegram message handler
def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    response = query_huggingface(user_message)
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)

# Streamlit UI
st.title('Hugging Face Telegram Bot')
st.write('This bot integrates Hugging Face models with Telegram.')

# Start the bot
def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I am your Hugging Face bot. Send me a message and I'll respond.")

start_handler = CommandHandler('start', start)
message_handler = MessageHandler(Filters.text & ~Filters.command, handle_message)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_handler)

updater.start_polling()

# Display the bot status in Streamlit
if st.button('Start Bot'):
    st.write('Bot is running...')
else:
    st.write('Click the button to start the bot.')
