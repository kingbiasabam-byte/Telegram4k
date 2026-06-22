from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import httpx

BOT_TOKEN = "8858004097:AAGCYCWhnPB8Egh2By1DoE0ra0smP42HWY0"
GROQ_API_KEY = "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"

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "به فارسی و دوستانه به تمام سوالات پاسخ بده."},
            {"role": "user", "content": user_text}
        ]
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            result = response.json()
            answer = result["choices"][0]["message"]["content"]
            await update.message.reply_text(answer)

    except httpx.HTTPStatusError as e:
        await update.message.reply_text(f"❌ خطا در ارتباط با سرور: {e.response.status_code}")
    except httpx.RequestError:
        await update.message.reply_text("❌ اتصال به سرور برقرار نشد. لطفاً دقایقی دیگر تلاش کنید.")
    except Exception as e:
        await update.message.reply_text(f"❌ خطای ناشناخته: {str(e)}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("ربات فعال شد...")
    app.run_polling()

if __name__ == "__main__":
    main()
