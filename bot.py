import os
import logging
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

async def filter_lopburi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """กรองเฉพาะข้อความที่มี 'ลพบุรี' และ 'ที่ตรวจพบ:'"""
    
    # ตรวจสอบว่าเป็นข้อความจาก chat ต้นทางหรือไม่
    if update.message and update.message.chat_id == SOURCE_CHAT_ID:
        message_text = update.message.text or ""
        
        # ตรวจสอบว่ามี "ที่ตรวจพบ:" และ "ลพบุรี"
        if "ที่ตรวจพบ:" in message_text and "ลพบุรี" in message_text:
            try:
                # ส่งต่อไปยัง chat เป้าหมาย
                await context.bot.send_message(
                    chat_id=TARGET_CHAT_ID,
                    text=f"🚨 แจ้งเตือนลพบุรี\n\n{message_text}"
                )
                logger.info(f"✅ ส่งข้อความลพบุรีแล้ว: {update.message.message_id}")
            except Exception as e:
                logger.error(f"❌ เกิดข้อผิดพลาด: {e}")
        else:
            logger.info("ℹ️ ข้อความไม่ใช่ลพบุรี - ข้าม")

def main():
    """เริ่มต้น bot"""
    logger.info("🤖 กำลังเริ่มต้น Lopburi Filter Bot...")
    logger.info(f"📍 Source Chat ID: {SOURCE_CHAT_ID}")
    logger.info(f"📍 Target Chat ID: {TARGET_CHAT_ID}")
    
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN ไม่ได้ตั้งค่า!")
        return
    
    if SOURCE_CHAT_ID == 0 or TARGET_CHAT_ID == 0:
        logger.error("❌ Chat IDs ไม่ได้ตั้งค่าถูกต้อง!")
        return
    
    # สร้าง Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # เพิ่ม Handler สำหรับรับข้อความ
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, filter_lopburi)
    )
    
    logger.info("✅ Bot พร้อมทำงาน - กำลังฟังข้อความ...")
    
    # รัน Bot แบบ polling
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )

if __name__ == '__main__':
    main()
