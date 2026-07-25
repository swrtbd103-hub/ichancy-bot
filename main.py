import random
import string
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.error import BadRequest

TOKEN = '8859921791:AAEmhEM_sOHIcfJzlTLuviVOmvlLiIdI-Ms'
CHANNEL_USERNAME = '@Semo_Robert'
SUPPORT_USERNAME = '@osama_00012'
WALLET_ADDRESS = '34b433f3fb241b53b8b16a1270addcd9'
BOT_NAME = 'Ichancy semo bot'

# تم تثبيت الـ file_id الخاص بـ الباركود الذي تم رفعه لبوتك
BARCODE_FILE_ID = 'AgACAgQAAxkBAAEs09NqZNO3O8d2qB2dIq5M2T5S1X0_tAACbQ9rG9c6KVPD4he09F_mLwEAAwIAA3kaAz0E'

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

def force_subscribe_keyboard():
    keyboard = [
        [InlineKeyboardButton("الانضمام للقناة 📢", url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}")],
        [InlineKeyboardButton("تم الاشتراك 🔄", callback_data='check_subscription')]
    ]
    return InlineKeyboardMarkup(keyboard)

def terms_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("موافقة ✅", callback_data='accept_terms'),
            InlineKeyboardButton("رفض ❌", callback_data='reject_terms')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def main_keyboard():
    keyboard = [
        [InlineKeyboardButton("Ichancy ⚡", callback_data='title_ichancy')],
        [
            InlineKeyboardButton("سحب رصيد 📬", callback_data='withdraw'),
            InlineKeyboardButton("شحن رصيد 📬", callback_data='charge')
        ],
        [
            InlineKeyboardButton("إهداء رصيد 🎁", callback_data='gift_balance'),
            InlineKeyboardButton("كود هدية 🎁", callback_data='gift_code')
        ],
        [
            InlineKeyboardButton("نظام الاحالات 💰", callback_data='referral_system'),
            InlineKeyboardButton("الجاكبوت 🎰", callback_data='jackpot')
        ],
        [
            InlineKeyboardButton("رسالة للأدمن ✉️", callback_data='msg_to_admin'),
            InlineKeyboardButton("تواصل معنا ✉️", callback_data='contact_us')
        ],
        [InlineKeyboardButton("البونات والعروض الحالية 🔥", callback_data='current_offers')],
        [
            InlineKeyboardButton("تشغيل كامل اقسام الموقع ↗️", callback_data='full_site_sections'),
            InlineKeyboardButton("ichancy apk ↗️", callback_data='ichancy_apk')
        ],
        [
            InlineKeyboardButton("الشروط والاحكام 📌", callback_data='terms'),
            InlineKeyboardButton("الشروحات 📌", callback_data='tutorials')
        ],
        [InlineKeyboardButton("السجل 🔄", callback_data='history')]
    ]
    return InlineKeyboardMarkup(keyboard)

def ichancy_keyboard():
    keyboard = [
        [InlineKeyboardButton("انشاء حساب جديد ⚡", callback_data='create_account')],
        [
            InlineKeyboardButton("سحب من حساب ⚡", callback_data='ichancy_withdraw'),
            InlineKeyboardButton("شحن حساب ⚡", callback_data='ichancy_deposit')
        ],
        [
            InlineKeyboardButton("💸 سحب كامل الرصيد", callback_data='withdraw_all'),
            InlineKeyboardButton("💰 شحن كامل الرصيد", callback_data='deposit_all')
        ],
        [InlineKeyboardButton("القائمة الرئيسية", callback_data='back_to_main')]
    ]
    return InlineKeyboardMarkup(keyboard)

def deposit_methods_keyboard():
    keyboard = [
        [InlineKeyboardButton("Sham Cash Auto ⚡(USD , SYP) (+ 5%)", callback_data='pay_sham_cash')],
        [InlineKeyboardButton("Syriatel Cash 🟢 (+ 5%)", callback_data='pay_syriatel')],
        [InlineKeyboardButton("Credit Card (+ 5%)", callback_data='pay_card')],
        [InlineKeyboardButton("عملات ومحافط رقمية ( USDT ) (+ 5%) ₮", callback_data='crypto_title')],
        [
            InlineKeyboardButton("USDT-TRC20 (+", callback_data='pay_usdt_trc20'),
            InlineKeyboardButton("USDT - BEP 20 🟡 Binance", callback_data='pay_usdt_bep20')
        ],
        [InlineKeyboardButton("القائمة الرئيسية", callback_data='back_to_main')]
    ]
    return InlineKeyboardMarkup(keyboard)

def sham_cash_keyboard():
    keyboard = [
        [InlineKeyboardButton("📱 عرض الباركود", callback_data='show_barcode')],
        [InlineKeyboardButton("رجوع", callback_data='charge')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_states[user_id] = None
    
    if not await is_subscribed(user_id, context):
        await update.message.reply_text(
            f"عذراً! يجب عليك الاشتراك في القناة أولاً لاستخدام البوت:\n{CHANNEL_USERNAME}",
            reply_markup=force_subscribe_keyboard()
        )
        return

    if user_id in verified_users:
        await update.message.reply_text(f"أهلا بك في بوت\n\n{BOT_NAME}", reply_markup=main_keyboard())
        return

    terms_text = (
        "عند الضغط على زر موافقة فأنت توافق على الشروط القائمة ضمن البوت ويحق لك الإعتراض في حال مواجهة أي مشكلة خارجة عن شروط وقوانين البوت "
        "يرجى قراءة هذه الشروط قبل استخدام البوت لضمان تجربة آمنة وسلسة.\n\n"
        "البوت مخصص لإنشاء الحسابات، والسحب، والتعبئة الفورية لحسابات موقع Ichancy.\n\n"
        "1_ منع الحسابات المتعددة:\nإنشاء أكثر من حساب للشخص الواحد مخالف للقوانين، وقد تؤدي إلى حظر الحسابات المرتبطة وتجميد أرصدتها، وذلك بناءً على سياسة اللعب النظيف.\n\n"
        "2_ تبديل طرق الدفع غير مسموح:\nلا يُسمح بشحن رصيد وسحبه بغرض التبديل بين وسائل الدفع المختلفة. في حال اكتشاف عملية كهذه، يتم سحب الرصيد والتحفظ عليه دون إشعار مسبق.\n\n"
        "3_ شروط أرباح الإحالات:\nتُحتسب أرباح الإحالة فقط بعد تسجيل 3 إحالات نشطة أو أكثر (أي قاموا بالتعبئة الفعلية).\n\n"
        "⚠️ تنبيه:\nأي محاولة للتحايل أو مخالفة الشروط ستؤدي إلى إيقاف الحساب وتجميد الأرصدة."
    )
    await update.message.reply_text(terms_text, reply_markup=terms_keyboard())

async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    verified_users.add(user_id)
    
    remove_kb = ReplyKeyboardRemove()
    await update.message.reply_text("تم تأكيد رقم الهاتف بنجاح يمكنك المتابعة", reply_markup=remove_kb)
    await update.message.reply_text("🎉 تم تفعيل البونص الترحيبي بنجاح تمت إضافة 5,000 ل.س إلى رصيدك.")

    await update.message.reply_text(f"أهلا بك في بوت\n\n{BOT_NAME}", reply_markup=main_keyboard())

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_states.get(user_id) == 'WAITING_FOR_ACCOUNT_NAME':
        account_name = update.message.text.strip()
        generated_pass = generate_password()
        
        user_states[user_id] = None
        
        response_text = (
            "✅ **تم إنشاء حساب إيشانسي بنجاح!**\n\n"
            f"👤 **الاسم:** {account_name}\n"
            f"🔑 **كلمة السر:** `{generated_pass}`\n\n"
            "يرجى حفظ البيانات في مكان آمن لاستخدامها في تسجيل الدخول."
        )
        await update.message.reply_text(response_text, parse_mode='Markdown', reply_markup=main_keyboard())
    else:
        await update.message.reply_text(f"أهلا بك في بوت\n\n{BOT_NAME}", reply_markup=main_keyboard())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == 'check_subscription':
        if await is_subscribed(user_id, context):
            await query.message.edit_text("تم التحقق بنجاح! أهلاً بك في البوت ⚡")
            await start(update, context)
        else:
            await query.answer("لم تشترك بعد! يرجى الانضمام للقناة أولاً.", show_alert=True)
        return

    if not await is_subscribed(user_id, context):
        await query.message.edit_text(
            f"عذراً! يجب عليك الاشتراك في القناة أولاً لاستخدام البوت:\n{CHANNEL_USERNAME}",
            reply_markup=force_subscribe_keyboard()
        )
        return

    if query.data == 'accept_terms':
        await query.message.edit_text("تم قبول الشروط، يمكنك المتابعة باستخدام البوت.")
        bonus_text = (
            "🎁 لديك بونص ترحيبي بقيمة 5,000 ل.س\n\n"
            "لتحصل عليه يجب تأكيد رقم هاتفك السوري من الزر بالأسفل.\n"
            "مهلة التفعيل المتبقية: 6 ساعة و 00 دقيقة\n"
            f"آخر وقت للتفعيل: {calculate_time()}"
        )
        contact_keyboard = [[{"text": "تأكيد رقم الحساب", "request_contact": True}]]
        await query.message.reply_text(bonus_text, reply_markup=ReplyKeyboardMarkup(contact_keyboard, resize_keyboard=True, one_time_keyboard=True))

    elif query.data == 'reject_terms':
        await query.message.edit_text("لا يمكنك استخدام البوت دون الموافقة على الشروط.")
    
    elif query.data == 'title_ichancy':
        await query.message.edit_text("اختر من القائمة أدناه:", reply_markup=ichancy_keyboard())

    elif query.data == 'create_account':
        user_states[user_id] = 'WAITING_FOR_ACCOUNT_NAME'
        await query.message.edit_text("ادخل اسم حساب ايشانسي")
        
    elif query.data == 'charge':
        await query.message.edit_text("قسم شحن الرصيد 📬:\nالرجاء إرسال المبلغ المطلوب شحنه أو تحديد احد طرق الشحن", reply_markup=deposit_methods_keyboard())
        
    elif query.data == 'pay_sham_cash':
        sham_cash_text = (
            f"ارسل الى العنوان\n\n{WALLET_ADDRESS}\n\n🔹 Lucky Tel ecom 🔹\n\n"
            "ثم ادخل رقم العملية\n\nلأي استفسار التواصل مع الدعم عبر المعرف التالي :\n"
            f"{SUPPORT_USERNAME}\n1 ShamCash USD = 13500"
        )
        await query.message.reply_text(sham_cash_text, reply_markup=sham_cash_keyboard())

    elif query.data == 'show_barcode':
        try:
            await query.message.reply_photo(
                photo=BARCODE_FILE_ID, 
                caption="باركود شام كاش\nاستخدم الباركود أدناه للشحن"
            )
        except Exception as e:
            await query.message.reply_text(f"تعذر عرض الصورة، يرجى المحاولة لاحقاً.\nالخطأ: {e}")

    elif query.data == 'back_to_main':
        await query.message.edit_text(f"أهلا بك في بوت\n\n{BOT_NAME}", reply_markup=main_keyboard())

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    
    print("البوت يعمل الآن...")
    app.run_polling()
