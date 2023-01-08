from ʜʏᴘᴇ_ʀᴇᴍᴏᴠᴇʀ_ʙᴏᴛ import dispatcher,FEEDBACK
from ʜᴏᴍᴇᴅɪʀ.miscl import paginate_modules
from ᴋᴀᴛᴇ import *
from FANCY import *

def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    dispatcher.bot.send_message(chat_id=chat_id,
                                text=text,
                                parse_mode=ParseMode.MARKDOWN,
                                reply_markup=keyboard)


run_async
def start(update: Update, context: CallbackContext):
    args = context.args
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, FUSE)
        else:
            update.effective_message.reply_photo(
                DEL_TER,
                caption=BRGIN,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="tambahkan ke grup",
                                url="t.me/{}?startgroup=botstart".format(context.bot.username),
                            )
                        ]
                    ]
                ),
            )
    else:
        ok = update.effective_message.reply_photo(DEL_TER,"♦️𝗡𝗼𝘁𝗲 𝗧𝗼 𝗔𝗱𝗺𝗶𝗻𝘀♦️\nJangan lupa beri saya hak admin hapus pesan.")
        ok.delete(timeout=10)


run_async
def help_button(update: Update, context: CallbackContext):
    args = context.args
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    try:
        if mod_match:
            module = mod_match.group(1)
            text = "Berikut adalah bantuan untuk *{}* modul:\n".format(HELPABLE[module].__element__) \
                   + HELPABLE[module].__help__
            query.message.edit_text(text=text,
                                     parse_mode=ParseMode.MARKDOWN,
                                     reply_markup=InlineKeyboardMarkup(
                                         [[InlineKeyboardButton(text="Back", callback_data="help_back")]]))

        elif prev_match:
            curr_page = int(prev_match.group(1))
            query.message.edit_text(FUSE,
                                     parse_mode=ParseMode.MARKDOWN,
                                     reply_markup=InlineKeyboardMarkup(
                                         paginate_modules(curr_page - 1, HELPABLE, "help")))

        elif next_match:
            next_page = int(next_match.group(1))
            query.message.edit_text(FUSE,
                                     parse_mode=ParseMode.MARKDOWN,
                                     reply_markup=InlineKeyboardMarkup(
                                         paginate_modules(next_page + 1, HELPABLE, "help")))

        elif back_match:
            query.message.edit_text(text=FUSE,
                                     parse_mode=ParseMode.MARKDOWN,
                                     reply_markup=InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help")))
        context.bot.answer_callback_query(query.id)
    except BadRequest as excp:
        if excp.message == "Pesan tidak diubah":
            pass
        elif excp.message == "Query_id_invalid":
            pass
        elif excp.message == "Pesan tidak bisa dihapus":
            pass
        else:
            FEEDBACK.exception("Pengecualian di tombol bantuan. %s", str(query.data))

run_async
def get_help(update: Update, context: CallbackContext):
    args = context.args
    chat = update.effective_chat
    if chat.type != chat.PRIVATE:
        update.effective_message.reply_text("Hubungi saya dalam PM untuk mendapatkan daftar perintah.",
                                            reply_markup=InlineKeyboardMarkup(
                                                [[InlineKeyboardButton(text="Help",
                                                                       url="t.me/{}?start=help".format(
                                                                           context.bot.username))]]))
        
        return
    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = "Here is the available help for the *{}* module:\n".format(HELPABLE[module].__element__) \
               + HELPABLE[module].__help__
        send_help(chat.id, text, InlineKeyboardMarkup([[InlineKeyboardButton(text="Back", callback_data="help_back")]]))
    else:
        send_help(chat.id, FUSE)
      
__element__ = "ready"
        
start_handler = CommandHandler("start", start, pass_args=True)
help_handler = CommandHandler("help", get_help)
help_callback_handler = CallbackQueryHandler(help_button, pattern=r"help_")


dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(help_callback_handler)
