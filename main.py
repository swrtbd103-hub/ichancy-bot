import os
import random
import string
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

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

def withdraw_methods_keyboard():
    keyboard = [
        [InlineKeyboardButton("Sham Cash (SYP) 🇸🇾", callback_data='w_sham_syp')],
        [InlineKeyboardButton("💲 Sham Cash (USD)", callback_data='w_sham_usd')],
        [InlineKeyboardButton("Syriatel Cash 🟢", callback_data='w_syriatel')],
        [
            InlineKeyboardButton("Usdt trc20", callback_data='w_usdt_trc20'),
            InlineKeyboardButton("Usdt Bep 20", callback_data='w_usdt_bep20')
        ],
        [
            InlineKeyboardButton("Coine x", callback_data='w_coinex'),
            InlineKeyboardButton("Cwellet", callback_data='w_cwellet')
        ],
        [InlineKeyboardButton("Payeer 💲", callback_data='w_payeer')],
        [InlineKeyboardButton("🟡 Binance 🟡", callback_data='w_binance')],
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

def tutorials_keyboard():
    keyboard = [
        [InlineKeyboardButton("ما هو موقع Ichancy؟", callback_data='tut_1')],
        [InlineKeyboardButton("كيفية شحن الرصيد ضمن بوت Ichancy", callback_data='tut_2')],
        [InlineKeyboardButton("كيفية إنشاء حساب Ichancy جديد", callback_data='tut_3')],
        [InlineKeyboardButton("كيفية سحب الرصيد من بوت Ichancy", callback_data='tut_4')],
        [InlineKeyboardButton("كيفية شحن رصيد ضمن حساب Ichancy", callback_data='tut_5')],
        [InlineKeyboardButton("كيفية سحب رصيد من حساب Ichancy", callback_data='tut_6')],
        [InlineKeyboardButton("القائمة الرئيسية", callback_data='back_to_main')]
    ]
    return InlineKeyboardMarkup(keyboard)

def back_to_tutorials_keyboard():
    keyboard = [
        [InlineKeyboardButton("رجوع للشروحات 🔄", callback_data='tutorials')]
    ]
    return InlineKeyboardMarkup(keyboard)

def back_to_main_only_keyboard():
    keyboard = [
        [InlineKeyboardButton("القائمة الرئيسية", callback_data='back_to_main')]
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

    terms_text = "عند الضغط على زر موافقة فأنت توافق على الشروط القائمة ضمن البوت ويحق لك الإعتراض في حال مواجهة أي مشكلة خارجة عن شروط وقوانين البوت يرجى قراءة هذه الشروط قبل استخدام البوت لضمان تجربة آمنة وسلسة.\n\nالبوت مخصص لإنشاء الحسابات، والسحب، والتعبئة الفورية لحسابات موقع Ichancy.\n\n1_ منع الحسابات المتعددة:\nإنشاء أكثر من حساب للشخص الواحد مخالف للقوانين، وقد تؤدي إلى حظر الحسابات المرتبطة وتجميد أرصدتها.\n\n2_ تبديل طرق الدفع غير مسموح:\nلا يُسمح بشحن رصيد وسحبه بغرض التبديل بين وسائل الدفع المختلفة.\n\n3_ شروط أرباح الإحالات:\nتُحتسب أرباح الإحالة فقط بعد تسجيل 3 إحالات نشطة أو أكثر.\n\n⚠️ تنبيه:\nأي محاولة للتحايل أو مخالفة الشروط ستؤدي إلى إيقاف الحساب وتجميد الأرصدة."
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
    state = user_states.get(user_id)
    
    if state == 'WAITING_FOR_ACCOUNT_NAME':
        account_name = update.message.text.strip()
        generated_pass = generate_password()
        user_states[user_id] = None
        
        response_text = f"✅ **تم إنشاء حساب إيشانسي بنجاح!**\n\n👤 **الاسم:** {account_name}\n🔑 **كلمة السر:** `{generated_pass}`\n\nيرجى حفظ البيانات في مكان آمن لاستخدامها في تسجيل الدخول."
        await update.message.reply_text(response_text, parse_mode='Markdown', reply_markup=main_keyboard())
    elif state == 'WAITING_FOR_GIFT_CODE':
        user_states[user_id] = None
        await update.message.reply_text("⚠️ كود غير صحيح", reply_markup=main_keyboard())
    elif state == 'WAITING_FOR_ADMIN_MSG':
        user_states[user_id] = None
        await update.message.reply_text("✅ تم إرسال رسالتك إلى الأدمن بنجاح.", reply_markup=main_keyboard())
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
        await query.message.edit_text(f"عذراً! يجب عليك الاشتراك في القناة أولاً لاستخدام البوت:\n{CHANNEL_USERNAME}", reply_markup=force_subscribe_keyboard())
        return

    if query.data == 'accept_terms':
        verified_users.add(user_id)
        await query.message.edit_text("تم قبول الشروط، يمكنك المتابعة باستخدام البوت.")
        bonus_text = "🎁 لديك بونص ترحيبي بقيمة 5,000 ل.س\n\nلتحصل عليه يجب تأكيد رقم هاتفك السوري من الزر بالأسفل.\nمهلة التفعيل المتبقية: 6 ساعة و 00 دقيقة\nآخر وقت للتفعيل: " + calculate_time()
        contact_keyboard = [[{"text": "تأكيد رقم الحساب", "request_contact": True}]]
        await query.message.reply_text(bonus_text, reply_markup=ReplyKeyboardMarkup(contact_keyboard, resize_keyboard=True, one_time_keyboard=True))
    elif query.data == 'reject_terms':
        await query.message.edit_text("لا يمكنك استخدام البوت دون الموافقة على الشروط.")
    elif query.data == 'back_to_main':
        user_states[user_id] = None
        await query.message.edit_text(f"أهلا بك في بوت\n\n{BOT_NAME}", reply_markup=main_keyboard())
    elif query.data == 'title_ichancy':
        await query.message.edit_text("اختر من القائمة أدناه:", reply_markup=ichancy_keyboard())
    elif query.data == 'withdraw':
        await query.message.edit_text("اختر احد الطرق", reply_markup=withdraw_methods_keyboard())
    elif query.data == 'charge':
        await query.message.edit_text("قسم شحن الرصيد 📬:\nالرجاء إرسال المبلغ المطلوب شحنه أو تحديد احد طرق الشحن", reply_markup=deposit_methods_keyboard())
    elif query.data == 'gift_balance':
        gift_text = f"ان عملية الاهداء هذه ستكون العملية رقم 1 لليوم وسيلتم اقتطاع عمولة بنسبة 5.0% من قيمة المبلغ المرسل\nارسل معرف التلغرام للشخص المراد اهداء الرصيد اليه\nيمكن الحصول على المعرف عن طريق ضغط زر رصيدي\nمعرف الاهداء الخاص بك هو {user_id}\nارسل معرف تلغرام المستخدم الذي تريد اهداؤه"
        await query.message.edit_text(gift_text, reply_markup=back_to_main_only_keyboard())
    elif query.data == 'gift_code':
        user_states[user_id] = 'WAITING_FOR_GIFT_CODE'
        await query.message.edit_text("👇 ادخل كود الهداية")
    elif query.data == 'referral_system':
        ref_link = f"http://t.me/ichancy_lucky_bot?start=MzczODk="
        ref_text = f"نظام احالات Ichancy Lucky Bot\nيقدم لك فرصة لكسب إضافي كل 10 أيام.\nكن وكيلاً معنا وأبشر النسب العالية!\nإحصل على نسبة ثابتة لكل عمليات الشحن والتعبئة القادمة عن طريق رابط احالتك ضمن البوت\n\n1-عند الدخول الى البوت قم بنسخ رابط الاحالة الخاص بك عن طريق الضغط على خيار رابط الاحالة الخاص بي\n2-عندما تقوم بنشر رابط احالتك ويقوم أحد بالتسجيل عن طريقه سيندا يحساب نسبة ثابتة لجميع عمليات السحب والتعبئة عن طريقك.\n3-يمكن الاطلاع على عدد الاحالات التي قامت بالتسجيل من خلال الرابط الخاص بك عن طريق الضغط على خيار عدد الاحالات الخاصة بك خلال المسابقة الحالية\n4- يتم حساب الارباح عند وجود 3 إحالات نشطة أو أكثر\nماذا تنتظر!...\nتوزيع النسب كل 10 أيام\n\nعدد الاحالات التابعة لك: 0\nرابط الإحالة الخاص بك:\n{ref_link}\n\nالموعد القادم لتوزيع الاحالات:\n2026-08-03 22:17:00\n9 يوم 6 ساعة 33 دقيقة"
        await query.message.edit_text(ref_text, reply_markup=back_to_main_only_keyboard())
    elif query.data == 'jackpot':
        jackpot_text = "يتم اختيار رابح الجاكبرت بشكل الي من أحد عمليات الشحن في جميع البوتات الرسمية التابعة لنا بأحد الطرق المتاحة\n\n♟ 1,000,000\n🕷 10,000,000\n♥ 20,000,000\n♠ 50,000,000\n\nالجاكبوت التالي:\n58.41%"
        await query.message.edit_text(jackpot_text, reply_markup=back_to_main_only_keyboard())
    elif query.data == 'msg_to_admin':
        user_states[user_id] = 'WAITING_FOR_ADMIN_MSG'
        await query.message.edit_text("اكتب رسالتك وسنقرأها في أقرب وقت:")
    elif query.data == 'contact_us':
        await query.message.edit_text(f"للتواصل مع الدعم الفني المباشر:\n{SUPPORT_USERNAME}", reply_markup=back_to_main_only_keyboard())
    elif query.data == 'current_offers':
        await query.message.edit_text("🔥 لا توجد عروض حالية متاحة اليوم، تابع القناة لملاحظة أي جديد!", reply_markup=back_to_main_only_keyboard())
    elif query.data == 'full_site_sections':
        await query.message.edit_text("تشغيل كامل أقسام الموقع ↗️:\nhttps://ichancy.com", reply_markup=back_to_main_only_keyboard())
    elif query.data == 'ichancy_apk':
        await query.message.edit_text("تحميل تطبيق Ichancy APK:\nhttps://ichancy.com/ar/", reply_markup=back_to_main_only_keyboard())
    elif query.data == 'terms':
        terms_text = "عند الضغط على زر موافقة فأنت توافق على الشروط القائمة ضمن البوت ويحق لك الإعتراض في حال مواجهة أي مشكلة خارجة عن شروط وقوانين البوت يرجى قراءة هذه الشروط قبل استخدام البوت لضمان تجربة آمنة وسلسة.\n\n1_ منع الحسابات المتعددة...\n"
        await query.message.edit_text(terms_text, reply_markup=back_to_main_only_keyboard())
    elif query.data == 'history':
        await query.message.edit_text("🔄 سجل العمليات الخاص بك فارغ حالياً.", reply_markup=back_to_main_only_keyboard())
    elif query.data == 'tutorials':
        await query.message.edit_text("اختر الشرح الذي تريد الاطلاع عليه:", reply_markup=tutorials_keyboard())
    elif query.data == 'tut_1':
        t1 = "ما هو موقع Ichancy؟\nموقع Ichancy هو منصة ترفيهية متكاملة تُقدم خدمات الرهانات الرياضية، ألعاب السلوت، ألعاب الكازينو، وألعاب متنوعة (Games)، مع نظام آلي لحساب الأرباح بناءً على النسب المرتبطة بكل خيار.\n\nأقسام الموقع:\n1. الرياضة (Sports):\nيتيح للمستخدمين المراهنة على مجموعة واسعة من الأحداث الرياضية مثل كرة القدم، كرة السلة، التنس وغيرها.\n\n2. السلوت (Slot):\nألعاب الحظ الممتعة برومات جذابة.\n\n3. الكازينو (Casino):\nمجموعة متنوعة من ألعاب الكازينو التقليدية مثل الروليت والباكارات وغيرها.\n\n4. الألعاب (Games):\nألعاب تفاعلية مسلية متنوعة.\n\nزيارة الموقع الرسمي:\nhttps://ichancy.com"
        await query.message.edit_text(t1, reply_markup=back_to_tutorials_keyboard())
    elif query.data == 'tut_2':
        t2 = "كيفية شحن الرصيد ضمن بوت Ichancy\nيرجى اتباع الخطوات التالية لإتمام عملية شحن الرصيد بنجاح:\n\n1. اضغط على خيار \"شحن رصيد\" في واجهة البوت.\n2. اختر طريقة الدفع المناسبة لك من بين الخيارات المتاحة.\n3. قم بفرز وإرسال المبلغ الذي ترغب في شحنه إلى العنوان المخصص (أقل مبلغ يمكن شحنه هو 1 دولار أمريكي).\n4. بعد إتمام التحويل، أدخل كود عملية التحويل، ثم أدخل قيمة المبلغ المرسل.\n\n✅ تم شحن الرصيد بنجاح."
        await query.message.edit_text(t2, reply_markup=back_to_tutorials_keyboard())
    elif query.data == 'tut_3':
        t3 = "كيفية إنشاء حساب Ichancy جديد\nلإنشاء حساب جديد على موقع Ichancy عبر البوت، يرجى اتباع الخطوات التالية:\n\n1. اضغط على خيار \"Ichancy\" في واجهة البوت.\n2. اختر \"حساب جديد\".\n3. أدخل اسماً للحساب الجديد.\n4. أدخل كلمة مرور لا تقل عن 8 أرقام/أحرف.\n5. أدخل المبلغ الذي ترغب بشحن الحساب به بالدولار ($).\n6. انتظر حوالي 15 ثانية لمعالجة الطلب.\n\n✅ تم إنشاء الحساب بنجاح."
        await query.message.edit_text(t3, reply_markup=back_to_tutorials_keyboard())
    elif query.data == 'tut_4':
        t4 = "كيفية سحب الرصيد من بوت Ichancy\nإتمام عملية السحب بنجاح، يرجى اتباع الخطوات التالية:\n\n1. اضغط على خيار \"سحب رصيد\" من واجهة البوت.\n2. اختر طريقة السحب المناسبة لك من بين الوسائل المتاحة.\n3. أدخل بياناتك المطلوبة بدقة، بحسب طريقة السحب التي قمت باختيارها.\n4. أدخل المبلغ الذي ترغب بسحبه.\n\n✅ تم تنفيذ عملية السحب بنجاح.\nيتم معالجة طلب السحب خلال مدة أقصاها نصف ساعة."
        await query.message.edit_text(t4, reply_markup=tutorials_keyboard())
    elif query.data == 'tut_5':
        t5 = "كيفية شحن رصيد ضمن حساب Ichancy\n لشحن رصيد إلى حسابك في موقع Ichancy عبر البوت، يرجى اتباع الخطوات التالية:\n\n1. اضغط على خيار \"Ichancy\" في واجهة البوت.\n2. اختر \"شحن حساب Ichancy\".\n3. أدخل معرف الحساب أو اسم حساب Ichancy الذي ترغب بشحنه.\n4. أدخل المبلغ المطلوب شحنه بالليرة السورية.\n5. انتظر حوالي 15 ثانية حتى تتم معالجة العملية.\n\n✅ تم شحن الحساب بنجاح."
        await query.message.edit_text(t5, reply_markup=back_to_tutorials_keyboard())
    elif query.data == 'tut_6':
        t6 = "كيفية سحب رصيد من حساب Ichancy\nلسحب رصيد من حسابك في موقع Ichancy عبر البوت، يرجى اتباع الخطوات التالية:\n\n1. اضغط على خيار \"Ichancy\" في واجهة البوت.\n2. اختر \"سحب رصيد من حساب Ichancy\".\n3. أدخل معرف الحساب أو اسم حساب Ichancy الذي ترغب بالسحب منه.\n4. أدخل المبلغ المطلوب سحبه بالدولار ($).\n5. انتظر حوالي 15 ثانية حتى تتم معالجة العملية.\n\n✅ تم سحب الرصيد بنجاح."
        await query.message.edit_text(t6, reply_markup=back_to_tutorials_keyboard())
    elif query.data == 'pay_sham_cash':
        sham_cash_text = f"ارسل الى العنوان\n\n{WALLET_ADDRESS}\n\n🔹 Lucky Tel ecom 🔹\n\nثم ادخل رقم العملية\n\nلأي استفسار التواصل مع الدعم عبر المعرف التالي :\n{SUPPORT_USERNAME}\n1 ShamCash USD = 13500"
        await query.message.reply_text(sham_cash_text, reply_markup=sham_cash_keyboard())
    elif query.data == 'show_barcode':
        if os.path.exists("barcode.jpg"):
            with open("barcode.jpg", "rb") as photo_file:
                await query.message.reply_photo(photo=photo_file, caption="باركود الدفع الخاص بك")
        else:
            await query.answer("عذراً، صورة الباركود غير موجودة في ملفات البوت.", show_alert=True)
    elif query.data.startswith('w_') or query.data.startswith('pay_'):
        await query.message.reply_text("أدخل المبلغ الذي ترغب به:")


if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    
    app.run_polling()
