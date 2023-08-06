import re
from telegram.ext import Updater
updater = Updater(token='542204492:AAFYvLsJ0br_ACodBUGEL1QsXURELPV-zak')

dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler


import telegram

import datetime

from . import HRauth
from . import HRlo
from . import HRget
from . import HRday
from . import utils

date_today = datetime.datetime.today()

hr_auth = HRauth.HRauth()
hr_get = HRget.HRget(hr_auth)

hr = HRlo.HRlo(hr_auth)

json = hr_get.get(year=date_today.year, month=date_today.month, day=date_today.day)
hr_today = HRday.HRday(json)

def get_today():
   json = hr_get.get(year=date_today.year, month=date_today.month, day=date_today.day)
   hr_today = HRday.HRday(json)
   return hr_today

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

def start(bot, update):
    keyboard = [
               [
                 InlineKeyboardButton("time", callback_data='time(bot, update)'),
                 InlineKeyboardButton("exit", callback_data='2'),
               ],
               [
                 InlineKeyboardButton("stamp", callback_data='2')
               ],
               [
                 InlineKeyboardButton("Option 3", callback_data='3')
               ]
               ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('HRlo commands:', reply_markup=reply_markup)


def stop(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="stop me please")
    updater.stop()

def bot_print(bot, update, msg):
    #msg = re.sub(r"[.\.]+", "\n", msg)
    bot.sendMessage(parse_mode='HTML', chat_id=update.message.chat_id, text='<pre>'+msg+'</pre>')
    #bot.send_message(chat_id=update.message.chat_id, text="`" + msg + "`", parse_mode=telegram.ParseMode.MARKDOWN)

def _message_format(msg):
    return re.sub(r"[.\.]+", "\n", msg)

def button(bot, update):
    query = update.callback_query

    bot.edit_message_text(text="Selected option: {}".format(query.data),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

def hrlo(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    msg = hr.report_day()
    msg = _message_format(msg)
    bot_print(bot, update, msg)

def day(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    msg = hr.report_day()
    msg = _message_format(msg)
    bot_print(bot, update, msg)

def week(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    msg = hr.report_week()
    msg = _message_format(msg)
    bot_print(bot, update, msg)

def week_month(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    msg = hr.report_month_weeks()
    msg = _message_format(msg)
    bot_print(bot, update, msg)

def month(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    msg = hr.report_month()
    msg = _message_format(msg)
    bot_print(bot, update, msg)

def exit(bot, update):
    hr_today = get_today()
    bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    msg = "Today estimated Exits\n"
    lunch = True
    least = False
    msg += "Standard time  [{}]\n  Exit  @ {}\n  Remains  {}\n".format(
            hr_today.HR_workday,
            str(hr_today.exit(lunch=lunch, least=least).strftime("%H:%M")),
            str(hr_today.remains(lunch=lunch, least=least)),
            )
    lunch = True
    least = True
    msg += "At Least lunch [{}]\n  Exit  @ {}\n  Remains  {}\n".format(
            hr_today.HR_workday_least_with_lunch,
            str(hr_today.exit(lunch=lunch, least=least).strftime("%H:%M")),
            str(hr_today.remains(lunch=lunch, least=least)),
            )
    lunch = False
    least = True
    msg += "At Least work  [{}]\n  Exit  @ {}\n  Remains  {}\n".format(
            hr_today.HR_workday_least,
            str(hr_today.exit(lunch=lunch, least=least).strftime("%H:%M")),
            str(hr_today.remains(lunch=lunch, least=least)),
            )
    bot_print(bot, update, msg)

def stamp(bot, update):
    hr_today = get_today()
    bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    msg = "Today Timestamps\n"
    msg += "[{}]\n".format( ", ".join([ i.time().strftime("%H:%M") for i in hr_today.logs()]))
    bot_print(bot, update, msg)

def time(bot, update):
    hr_today = get_today()
    bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    msg = "Today Times\n"
    msg += "Uptime         {}\n".format(hr_today.uptime())
    msg += "Worked time %  {:.1f}\n".format( 100.0*hr_today.uptime().total_seconds()/hr_today.time_to_work())
    msg += "Time to work   {}\n".format(utils.to_str(hr_today.time_to_work()))
    msg += "Timenet        {}\n".format(utils.to_str(hr_today.timenet()))
    msg += "Lunch time     {}\n".format(utils.to_str(hr_today['time_lunch']))
    msg += "KO time        {}\n".format(utils.to_str(hr_today['time_ko']))
    bot_print(bot, update, msg)
    return msg

def in_presence(bot, update, workers):
    msg = workers
    bot_print(bot, update, msg)

def help(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    msg = """HRlo_bot help
/day
/week
/week_month
/month

/exit
/stamp
/time
    """
    bot_print(bot, update, msg)

def main():
    msg = hr.report_day()
    msg = str(hr_today)
    msg = re.sub(r"[\.]+", "\n", msg)
    print(msg)
    #print(hr.day())
    #print(type(hr.week()))


    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)

    stop_handler = CommandHandler('stop', stop)
    dispatcher.add_handler(stop_handler)

    dispatcher.add_handler( CommandHandler('start', start) )

    dispatcher.add_handler( CommandHandler('day', day) )
    dispatcher.add_handler( CommandHandler('week', week) )
    dispatcher.add_handler( CommandHandler('week_month', week_month) )
    dispatcher.add_handler( CommandHandler('month', month) )

    dispatcher.add_handler( CommandHandler('exit', exit) )
    dispatcher.add_handler( CommandHandler('stamp', stamp) )
    dispatcher.add_handler( CommandHandler('time', time) )

    dispatcher.add_handler( CommandHandler('help', help) )

    #dispatcher.add_handler( CommandHandler('in', in_presence, pass_workers=True) )

    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
   main()

