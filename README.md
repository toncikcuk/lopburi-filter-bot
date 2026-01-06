# Lopburi Filter Bot

Bot สำหรับกรองข้อความที่มีคำว่า "ลพบุรี" และ "ที่ตรวจพบ:" แล้วส่งต่อไปยัง chat อื่น

## วิธีการติดตั้งบน Render

### 1. เตรียมข้อมูล
- Bot Token จาก @BotFather
- Source Chat ID (chat ที่รับข้อความทั้งหมด)
- Target Chat ID (chat ที่จะแจ้งเตือนเฉพาะลพบุรี)

### 2. สร้าง GitHub Repository
1. สร้างบัญชี GitHub (ถ้ายังไม่มี): https://github.com/signup
2. สร้าง Repository ใหม่ชื่อ "lopburi-filter-bot"
3. อัพโหลดไฟล์ 3 ไฟล์นี้:
   - bot.py
   - requirements.txt
   - render.yaml

### 3. Deploy บน Render
1. สมัครบัญชี Render (ฟรี): https://render.com/
2. กด "New +" → "Background Worker"
3. เชื่อมต่อกับ GitHub Repository ของคุณ
4. Render จะตรวจพบ render.yaml อัตโนมัติ
5. เพิ่ม Environment Variables:
   - BOT_TOKEN = <token ของคุณ>
   - SOURCE_CHAT_ID = <chat ID ต้นทาง>
   - TARGET_CHAT_ID = <chat ID ปลายทาง>
6. กด "Create Background Worker"

### 4. เสร็จสิ้น!
Bot จะทำงานตลอด 24/7 โดยอัตโนมัติ

## การทดสอบ
1. ส่งข้อความที่มี "ที่ตรวจพบ:" และ "ลพบุรี" ใน Source Chat
2. ตรวจสอบว่า Bot ส่งข้อความไปที่ Target Chat หรือไม่

## หมายเหตุ
- Render แพลนฟรีจะหยุดทำงานหลัง 15 นาทีที่ไม่มีการใช้งาน แต่จะกลับมาทำงานอัตโนมัติเมื่อมีข้อความใหม่
- ถ้าต้องการให้ทำงานตลอดเวลา ใช้ UptimeRobot (ฟรี) เพื่อ ping ทุก 5 นาที
