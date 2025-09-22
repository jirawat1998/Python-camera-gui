import cv2
import tkinter as tk
from tkinter import Label, Button, filedialog, Toplevel
from PIL import Image, ImageTk
import datetime
import os

# กล้อง (0 = กล้องหลักของ notebook)
cap = cv2.VideoCapture(0)

# GUI หลัก
root = tk.Tk()
root.title("Camera Preview")
root.geometry("800x600")

label = Label(root)
label.pack()

# ตัวแปรสถานะ
is_previewing = False
save_dir = os.getcwd()  # ค่าเริ่มต้น = โฟลเดอร์ที่รัน script
last_captured_frame = None  # เก็บ frame ล่าสุดที่ถ่ายได้

def show_frame():
    global is_previewing
    if is_previewing:
        ret, frame = cap.read()
        if ret:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            label.imgtk = imgtk
            label.configure(image=imgtk)
        label.after(10, show_frame)

def start_camera():
    global is_previewing
    is_previewing = True
    show_frame()

def stop_camera():
    global is_previewing
    is_previewing = False
    label.configure(image="")  # เคลียร์ภาพ

def capture_image():
    global last_captured_frame
    ret, frame = cap.read()
    if ret:
        last_captured_frame = frame
        show_preview_popup(frame)

def show_preview_popup(frame):
    # สร้าง popup สำหรับพรีวิวภาพ
    popup = Toplevel(root)
    popup.title("Preview")
    
    # แปลงเป็นรูปสำหรับแสดงผล
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    
    lbl_preview = Label(popup, image=imgtk)
    lbl_preview.image = imgtk  # กัน gc
    lbl_preview.pack()

    def save_image():
        global save_dir, last_captured_frame
        if last_captured_frame is not None:
            filename = f"capture_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            filepath = os.path.join(save_dir, filename)
            cv2.imwrite(filepath, last_captured_frame)
            print(f"✅ บันทึกภาพเป็น {filepath}")
        popup.destroy()

    def retake_image():
        popup.destroy()

    btn_save = Button(popup, text="✔️ Save", command=save_image)
    btn_save.pack(side="left", padx=10, pady=10)

    btn_retake = Button(popup, text="🔄 ถ่ายใหม่", command=retake_image)
    btn_retake.pack(side="right", padx=10, pady=10)

def choose_directory():
    global save_dir
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        save_dir = folder_selected
        print(f"📂 โฟลเดอร์ที่เลือก: {save_dir}")

def close_app():
    global is_previewing
    is_previewing = False
    cap.release()
    root.destroy()

# ปุ่ม
btn_start = Button(root, text="📷 เปิดกล้อง", command=start_camera)
btn_start.pack(pady=5)

btn_stop = Button(root, text="🛑 ปิดกล้อง", command=stop_camera)
btn_stop.pack(pady=5)

btn_capture = Button(root, text="📌 ถ่ายภาพ", command=capture_image)
btn_capture.pack(pady=5)

btn_choose_dir = Button(root, text="📂 เลือกโฟลเดอร์เซฟ", command=choose_directory)
btn_choose_dir.pack(pady=5)

btn_exit = Button(root, text="❌ ปิดโปรแกรม", command=close_app)
btn_exit.pack(pady=5)

root.mainloop()
