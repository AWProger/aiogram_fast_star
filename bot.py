import asyncio  # Импортируем модуль asyncio для работы с асинхронным программированием
import logging  # Импортируем модуль для ведения логов
import os  # Импортируем модуль для работы с операционной системой
from aiogram import Bot, Dispatcher  # Импортируем классы Bot и Dispatcher из библиотеки aiogram
from dotenv import load_dotenv, find_dotenv  # Импортируем функции для загрузки переменных окружения из .env файла

# Загрузка переменных окружения из .env файла
load_dotenv(find_dotenv())  # Загружаем переменные окружения из файла .env
admins = os.getenv("ADMINS").split(',')  # Получаем список администраторов из переменной окружения
bot = Bot(token=os.getenv("TOKEN"))  # Инициализируем объект бота с токеном из переменной окружения
dp = Dispatcher(bot)  # Создаем диспетчер для обработки сообщений бота

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)  # Создаем логгер с именем текущего модуля

async def start_bot():
    logger.info("Бот успешно запущен.")  # Логируем информацию о запуске бота
    try:
        for admin in admins:  # Перебираем всех администраторов
            await bot.send_message(admin, 'Бот запущен')  # Отправляем сообщение о запуске бота каждому администратору
    except Exception as e:  # Обрабатываем исключения
        logger.error(f"Ошибка при отправке сообщения админам: {e}")  # Логируем ошибку

async def stop_bot():
    logger.info("Бот останавливается...")  # Логируем информацию о остановке бота
    try:
        for admin in admins:  # Перебираем всех администраторов
            await bot.send_message(admin, 'Бот остановлен.')  # Отправляем сообщение о остановке бота каждому администратору
    except Exception as e:  # Обрабатываем исключения
        logger.error(f"Ошибка при отправке сообщения админам: {e}")  # Логируем ошибку

async def main():
    logger.info("Запуск бота...")  # Логируем информацию о запуске бота

    try:
        # Запуск бота
        await start_bot()  # Вызываем функцию для отправки сообщений о запуске бота

        await bot.delete_webhook(drop_pending_updates=True)  # Удаляем вебхук (если он был установлен) и сбрасываем ожидающие обновления
        await dp.start_polling()  # Запускаем процесс получения обновлений
    except Exception as e:  # Обрабатываем исключения
        logger.error(f"Ошибка при запуске бота: {e}")  # Логируем ошибку
    finally:
        await stop_bot()  # Вызываем функцию остановки бота
        await bot.session.close()  # Закрываем сессию бота
        logger.info("Бот остановлен.")  # Логируем информацию о том, что бот остановлен

if __name__ == "__main__":  # Проверяем, запущен ли скрипт напрямую
    try:
        asyncio.run(main())  # Запускаем главную асинхронную функцию
    except (KeyboardInterrupt, SystemExit):  # Обрабатываем исключения, связанные с остановкой бота
        logger.info("Бот был остановлен вручную.")  # Логируем информацию о ручной остановке бота
