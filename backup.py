import os
import shutil
import smtplib
from email.message import EmailMessage
from datetime import datetime
from dotenv import load_dotenv

# Nạp biến môi trường từ file .env
load_dotenv()

# Lấy thông tin từ file .env
thu_muc_nguon = os.getenv("SOURCE_DIR")
thu_muc_backup = os.getenv("BACKUP_DIR")
email_gui = os.getenv("SENDER_EMAIL")
mat_khau = os.getenv("SENDER_PASSWORD")
email_nhan = os.getenv("RECEIVER_EMAIL")

# Hàm gửi email thông báo
def gui_email(tieu_de, noi_dung):
    msg = EmailMessage()
    msg["Subject"] = tieu_de
    msg["From"] = email_gui
    msg["To"] = email_nhan
    msg.set_content(noi_dung)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(email_gui, mat_khau)
            smtp.send_message(msg)
        print("Đã gửi email thông báo.")
    except Exception as loi:
        print("Lỗi khi gửi email:", loi)

# Hàm sao lưu file
def sao_luu():
    ngay = datetime.now().strftime("%Y-%m-%d")
    duong_dan_luu = os.path.join(thu_muc_backup, ngay)
    os.makedirs(duong_dan_luu, exist_ok=True)

    da_tim_thay = False

    try:
        for ten_file in os.listdir(thu_muc_nguon):
            if ten_file.endswith(".sql") or ten_file.endswith(".sqlite3"):
                duong_dan_file = os.path.join(thu_muc_nguon, ten_file)
                noi_luu = os.path.join(duong_dan_luu, ten_file)
                shutil.copy2(duong_dan_file, noi_luu)
                da_tim_thay = True

        if da_tim_thay:
            gui_email("✅ Sao lưu thành công", f"Đã sao lưu file vào: {duong_dan_luu}")
        else:
            gui_email("⚠️ Không có file sao lưu", "Không tìm thấy file .sql hoặc .sqlite3 nào.")
    except Exception as loi:
        gui_email("❌ Lỗi sao lưu", f"Gặp lỗi: {loi}")

# Gọi hàm khi chạy file
if __name__ == "__main__":
    sao_luu()
