import os
import asyncio
from telegram import Bot, Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

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
                print(f"✅ ส่งข้อความลพบุรีแล้ว: {update.message.message_id}")
            except Exception as e:
                print(f"❌ เกิดข้อผิดพลาด: {e}")
        else:
            print(f"ℹ️ ข้อความไม่ใช่ลพบุรี - ข้าม")

def main():
    """เริ่มต้น bot"""
    print("🤖 กำลังเริ่มต้น Bot...")
    print(f"📍 Source Chat ID: {SOURCE_CHAT_ID}")
    print(f"📍 Target Chat ID: {TARGET_CHAT_ID}")
    
    # สร้าง Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # เพิ่ม Handler สำหรับรับข้อความ
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, filter_lopburi)
    )
    
    print("✅ Bot พร้อมทำงาน - กำลังฟังข้อความ...")
    
    # รัน Bot
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )

if __name__ == '__main__':
    main()
