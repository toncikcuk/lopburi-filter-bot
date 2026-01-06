FROM python:3.11-slim

# ตั้งค่า working directory
WORKDIR /app

# ติดตั้ง dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy โค้ด
COPY bot.py .

# รัน bot
CMD ["python", "bot.py"]
