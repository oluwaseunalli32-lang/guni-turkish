import os
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      LinkPreviewOptions, Update)
from telegram.constants import ParseMode
from telegram.ext import (Application, CallbackQueryHandler,
                          CommandHandler, ContextTypes)

TOKEN = os.environ["BOT_TOKEN"]
BOT_NAME = "Güncel Bağlantı Rehberi"

# (name, short description, link)
CATEGORIES = {
    "ai": ("Yapay Zeka Araçları", [
        ("ChatGPT", "Sorulara yanıt veren, metin yazmaya yardım eden sohbet asistanı.", "https://chatgpt.com"),
        ("Claude", "Uzun metinleri özetleyen ve yazı çalışmalarında destek olan yapay zeka asistanı.", "https://claude.ai"),
        ("Gemini", "Google'ın sohbet asistanı; arama ve günlük işlerde yardımcı olur.", "https://gemini.google.com"),
        ("Canva", "Afiş, sunum ve sosyal medya görseli hazırlamak için tasarım aracı.", "https://www.canva.com"),
    ]),
    "sites": ("Faydalı Siteler", [
        ("Google Çeviri", "Metin ve web sayfalarını birçok dile çevirir.", "https://translate.google.com"),
        ("TinyPNG", "Görsellerin dosya boyutunu kaliteyi bozmadan küçültür.", "https://tinypng.com"),
        ("iLovePDF", "PDF birleştirme, bölme ve sıkıştırma işlemleri yapar.", "https://www.ilovepdf.com"),
        ("Wayback Machine", "Web sitelerinin eski sürümlerini arşivden gösterir.", "https://web.archive.org"),
    ]),
    "courses": ("Ücretsiz Kurslar", [
        ("freeCodeCamp", "Web geliştirme ve programlama için ücretsiz uygulamalı dersler.", "https://www.freecodecamp.org"),
        ("Khan Academy", "Matematik, bilim ve ekonomi konularında ücretsiz ders videoları.", "https://www.khanacademy.org"),
        ("MIT OpenCourseWare", "MIT derslerinin ücretsiz ders notları ve materyalleri.", "https://ocw.mit.edu"),
        ("CS50", "Harvard'ın ücretsiz bilgisayar bilimlerine giriş dersi.", "https://cs50.harvard.edu"),
    ]),
    "jobs": ("İş Kaynakları", [
        ("Kariyer.net", "Türkiye'de iş ilanlarına bakmak ve başvuru yapmak için site.", "https://www.kariyer.net"),
        ("İŞKUR", "Kamu istihdam kurumunun iş ilanları ve kurs duyuruları.", "https://www.iskur.gov.tr"),
        ("LinkedIn İş İlanları", "Profil oluşturup dünya genelinde ilanlara başvurma imkânı.", "https://www.linkedin.com/jobs/"),
        ("Remote OK", "Uzaktan çalışma ilanlarının listelendiği site.", "https://remoteok.com"),
    ]),
}

NO_PREVIEW = LinkPreviewOptions(is_disabled=True)

WELCOME = (
    f"<b>{BOT_NAME}</b>'ne hoş geldiniz.\n\n"
    "Yapay zeka araçları, faydalı siteler, ücretsiz kurslar ve iş kaynakları "
    "için açıklamalı bağlantılar burada. Bir kategori seçin:"
)


def menu_markup() -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(title, callback_data=key)]
            for key, (title, _) in CATEGORIES.items()]
    return InlineKeyboardMarkup(rows)


def category_text(key: str) -> str:
    title, items = CATEGORIES[key]
    lines = [f"<b>{BOT_NAME}</b> | {title}\n"]
    for name, desc, url in items:
        lines.append(f'• <a href="{url}">{name}</a> - {desc}')
    lines.append(f"\n{BOT_NAME} - başka bir kategori için aşağıdaki düğmeyi kullanın.")
    return "\n".join(lines)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        WELCOME, parse_mode=ParseMode.HTML, reply_markup=menu_markup())


async def show_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    back = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Kategorilere dön", callback_data="menu")]])
    await query.edit_message_text(
        category_text(query.data),
        parse_mode=ParseMode.HTML,
        link_preview_options=NO_PREVIEW,
        reply_markup=back,
    )


async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        WELCOME, parse_mode=ParseMode.HTML, reply_markup=menu_markup())


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler(["start", "menu"], start))
    app.add_handler(CallbackQueryHandler(back_to_menu, pattern="^menu$"))
    app.add_handler(CallbackQueryHandler(
        show_category, pattern="^(" + "|".join(CATEGORIES) + ")$"))
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
