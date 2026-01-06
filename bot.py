import os
import logging
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# ตั้งค่า logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ดึงค่าจากตัวแปร Environment
BOT_TOKEN = os.environ.get("BOT_TOKEN")
SOURCE_CHAT_ID = int(os.environ.get("SOURCE_CHAT_ID", "0"))
TARGET_CHAT_ID = int(os.environ.get("TARGET_CHAT_ID", "0"))

# สร้าง Flask app สำหรับ Web Service
app = Flask(__name__)

@app.route('/')
def home():
    """หน้าแรก - สำหรับ health check"""
    return """
    <html>
    <head><title>Lopburi Filter Bot</title></head>
    <body style="font-family: Arial; padding: 20px;">
        <h1>🤖 Lopburi Filter Bot</h1>
        <p>✅ Bot กำลังทำงาน</p>
        <hr>
        <p><strong>Status:</strong> Running</p>
        <p><strong>Source Chat ID:</strong> {}</p>
        <p><strong>Target Chat ID:</strong> {}</p>
    </body>
    </html>
    """.format(SOURCE_CHAT_ID, TARGET_CHAT_ID), 200

@app.route('/health')
def health():
    """Health check endpoint สำหรับ UptimeRobot"""
    return "OK", 200

@app.route('/status')
def status():
    """แสดงสถานะ Bot แบบ JSON"""
    return {
        "status": "running",
        "bot": "Lopburi Filter Bot",
        "source_chat_id": SOURCE_CHAT_ID,
        "target_chat_id": TARGET_CHAT_ID
    }, 200

def run_flask():
    """รัน Flask server"""
    port = int(os.environ.get("PORT", 10000))
    logger.info(f"🌐 เริ่ม Flask server บน port {port}")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

async def filter_lopburi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """กรองเฉพาะข้อความที่มี 'ลพบุรี' และ 'ที่ตรวจพบ:'"""
    
    # ตรวจสอบว่ามีข้อความหรือไม่
    if not update.message:
        return
    
    # ตรวจสอบว่าเป็นข้อความจาก chat ต้นทางหรือไม่
    if update.message.chat_id != SOURCE_CHAT_ID:
        logger.debug(f"ข้อความจาก chat อื่น (ID: {update.message.chat_id})")
        return
    
    message_text = update.message.text or ""
    
    # ตรวจสอบว่ามี "ที่ตรวจพบ:" และ "ลพบุรี"
    if "ที่ตรวจพบ:" in message_text and "ลพบุรี" in message_text:
        try:
            # ส่งต่อไปยัง chat เป้าหมาย
            await context.bot.send_message(
                chat_id=TARGET_CHAT_ID,
                text=f"🚨 แจ้งเตือนลพบุรี\n\n{message_text}"
            )
            logger.info(f"✅ ส่งข้อความลพบุรีแล้ว (Message ID: {update.message.message_id})")
        except Exception as e:
            logger.error(f"❌ เกิดข้อผิดพลาดในการส่งข้อความ: {e}")
    else:
        logger.debug("ℹ️ ข้อความไม่ใช่ลพบุรี - ข้าม")

def run_telegram_bot():
    """รัน Telegram Bot"""
    logger.info("🤖 กำลังเริ่มต้น Telegram Bot...")
    logger.info(f"📍 Source Chat ID: {SOURCE_CHAT_ID}")
    logger.info(f"📍 Target Chat ID: {TARGET_CHAT_ID}")
    
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN ไม่ได้ตั้งค่า!")
        return
    
    if SOURCE_CHAT_ID == 0 or TARGET_CHAT_ID == 0:
        logger.error("❌ Chat IDs ไม่ได้ตั้งค่าถูกต้อง!")
        return
    
    # สร้าง Telegram Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # เพิ่ม Handler สำหรับรับข้อความ
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, filter_lopburi)
    )
    
    logger.info("✅ Telegram Bot พร้อมทำงาน - กำลังฟังข้อความ...")
    
    # รัน Bot แบบ polling
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )

def main():
    """ฟังก์ชันหลัก - รัน Flask และ Telegram Bot พร้อมกัน"""
    logger.info("=" * 50)
    logger.info("🚀 เริ่มต้น Lopburi Filter Bot")
    logger.info("=" * 50)
    
    # รัน Flask server ใน thread แยก
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # รอให้ Flask เริ่มทำงาน
    import time
    time.sleep(2)
    
    # รัน Telegram Bot (blocking)
    run_telegram_bot()

if __name__ == '__main__':
    main()
