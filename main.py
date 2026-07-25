import os
import random
import string
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

# ضع التوكن الصحيح الجديد الخاص ببوتك هنا بين علامتي التنصيص
TOKEN = '8859921791:AAEmhEM_sOHIcfJzlTLuviVOmvlLiIdI-Ms'
CHANNEL_USERNAME = '@Semo_Robert'
SUPPORT_USERNAME = '@osama_00012'
WALLET_ADDRESS = '34b433f3fb241b53b8b16a1270addcd9'
BOT_NAME = 'Ichancy semo bot'

verified_users = set()
user_states = {}

def calculate_time(hours=6):
    future_time = datetime.now() + timedelta(hours=hours)
    return future_time.strftime('%H:%M:%S %d-%m-%Y')

def generate_password(length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

async def is_subscribed(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not await is_subscribed(user_id, context):
        keyboard_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("اشترك في القناة", url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}")],
            [InlineKeyboardButton("تحقق من الاشتراك", callback_data="check_sub")]
        ])
        await update.message.reply_text("عذراً، يجب عليك الاشتراك في قناة البوت أولاً لاستخدامه:\n" + CHANNEL_USERNAME, reply_markup=keyboard_markup)
        return

    verified_users.add(user_id)
    await show_main_menu(update, context)

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("شحن رصيد", callback_data="top_up")],
        [InlineKeyboardButton("حسابي", callback_data="my_account")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text("مرحباً بك في القائمة الرئيسية:", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.edit_text("مرحباً بك في القائمة الرئيسية:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "check_sub":
        if await is_subscribed(user_id, context):
            verified_users.add(user_id)
            await query.message.delete()
            await show_main_menu(update, context)
        else:
            await query.answer("لم تقم بالاشتراك بعد!", show_alert=True)
            
    elif query.data == "top_up":
        keyboard = [
            [InlineKeyboardButton("Credit Card (+ 5%)", callback_data="pay_cc")],
            [InlineKeyboardButton("USDT-TRC20 / BEP20", callback_data="pay_usdt")],
            [InlineKeyboardButton("رجوع", callback_data="main_menu")]
        ]
        await query.message.edit_text("اختر طريقة الشحن المناسبة:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "pay_cc" or query.data == "pay_usdt":
        keyboard = [[InlineKeyboardButton("عرض الباركود", callback_data="show_barcode")],
                     [InlineKeyboardButton("رجوع", callback_data="top_up")]]
        
        text = f"ارسل الى العنوان:\n`{WALLET_ADDRESS}`\n\n◆ Lucky Telecom ◆\n\nثم ادخل رقم العملية\n\nلأي استفسار التواصل مع الدعم عبر المعرف التالي :\n{SUPPORT_USERNAME}\n1 ShamCash USD = 13500"
        await query.message.edit_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "show_barcode":
        if os.path.exists("barcode.jpg"):
            with open("barcode.jpg", "rb") as photo_file:
                await context.bot.send_photo(chat_id=query.message.chat_id, photo=photo_file, caption="باركود الدفع الخاص بك")
        else:
            await query.answer("عذراً، صورة الباركود غير موجودة في ملفات البوت.", show_alert=True)

    elif query.data == "my_account":
        keyboard = [[InlineKeyboardButton("رجوع", callback_data="main_menu")]]
        await query.message.edit_text(f"معلومات الحساب:\nID: {user_id}\nالحالة: مفعل", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "main_menu":
        await show_main_menu(update, context)

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
