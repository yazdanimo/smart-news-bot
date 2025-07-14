import os
import threading
from dotenv import load_dotenv
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters
)
from db import is_duplicate, save_message
import logging
