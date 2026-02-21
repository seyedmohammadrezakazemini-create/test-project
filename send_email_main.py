import tkinter as tk
from tkinter import messagebox, scrolledtext
import smtplib
from email.mime.text import MIMEText
import json
from datetime import datetime


def send_emails():
    """تابع ارسال ایمیل‌ها"""
    # دریافت اطلاعات از فیلدها
    sender = email_entry.get()
    password = pass_entry.get()
    subject = subject_entry.get()
    message = text_area.get("1.0", tk.END)
    receivers = receivers_text.get("1.0", tk.END).strip().split("\n")

    # اعتبارسنجی فیلد ها
    if not all([sender, password, subject, message.strip()]):
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    if not receivers or not receivers[0]:
        messagebox.showerror("Error", "Enter at least one Gmail recipient.")
        return

    # تایید ارسال
    confirm = messagebox.askyesno(
        "Okay", f"Are you sure you want to send to{len(receivers)}"
    )
    if not confirm:
        return

    # ارسال ایمیل‌ها
    sent = 0
    failed = 0

    try:
        # اتصال به سرور
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        server.starttls()
        server.login(sender, password)

        status_label.config(text="Sending...", fg="orange")

        for receiver in receivers:
            receiver = receiver.strip()
            if not receiver or "@" not in receiver:
                continue

            try:
                # ساخت ایمیل
                msg = MIMEText(message, "plain", "utf-8")
                msg["Subject"] = subject
                msg["From"] = sender
                msg["To"] = receiver

                # ارسال
                server.send_message(msg)
                sent += 1

                # نمایش در کنسول
                log_area.insert(tk.END, f"✓ Sent to: {receiver}\n")

            except Exception as e:
                failed += 1
                log_area.insert(tk.END, f"✗ Error for {receiver}: {str(e)[:50]}\n")

            log_area.see(tk.END)
            window.update()

        # بستن اتصال
        server.quit()

        # نمایش نتیجه
        status_label.config(
            text=f"Compelet success: {sent}، Unsuccessful: {failed}", fg="green"
        )
        messagebox.showinfo(
            "Success", f"Complete!\n\nSuccess: {sent}\nUnsuccessful: {failed}"
        )

        # ذخیره تاریخچه
        save_history(subject, sent, failed)

    except Exception as e:
        status_label.config(text="Error sendings", fg="red")
        messagebox.showerror("Error", f"Error sendings:\n{str(e)}")


def save_history(subject, sent, failed):
    """ذخیره تاریخچه"""
    try:
        history = []
        try:
            with open("history.json", "r") as f:
                history = json.load(f)
        except:
            pass

        history.append(
            {
                "date": datetime.now().strftime("%Y/%m/%d %H:%M"),
                "subject": subject,
                "sent": sent,
                "failed": failed,
            }
        )

        with open("history.json", "w") as f:
            json.dump(history, f, indent=2)

    except:
        pass


def clear_fields():
    """پاک کردن فیلدها"""
    subject_entry.delete(0, tk.END)
    text_area.delete("1.0", tk.END)
    log_area.delete("1.0", tk.END)
    status_label.config(text="Ready", fg="green")


# ساخت پنجره اصلی
window = tk.Tk()
window.title("Send email")
window.geometry("700x800")
window.config(bg="#91a4bc")

# فونت
font_normal = ("lnter", 11, "bold")

# فریم تنظیمات
settings_frame = tk.LabelFrame(
    window, text="Transmitter settings", bg="#91a4bc", font=font_normal
)
settings_frame.pack(fill="x", padx=10, pady=5)

tk.Label(settings_frame, text="Sender email:", bg="#91a4bc", font=font_normal).pack(
    anchor="w", padx=5
)
email_entry = tk.Entry(
    settings_frame,
    bg="#008744",
    fg="white",
    font=font_normal,
    width=40,
    insertbackground="white",
)
email_entry.pack(fill="x", padx=5, pady=2)

tk.Label(settings_frame, text="App password:", bg="#91a4bc", font=font_normal).pack(
    anchor="w", padx=5
)

pass_entry = tk.Entry(
    settings_frame,
    bg="#008744",
    fg="white",
    font=font_normal,
    width=40,
    show="•",
    insertbackground="white",
)

pass_entry.pack(fill="x", padx=5, pady=2)

# فریم ایمیل
email_frame = tk.LabelFrame(
    window, text="Email details", bg="#91a4bc", font=font_normal
)
email_frame.pack(fill="x", padx=10, pady=5)

tk.Label(email_frame, text="Subjext:", bg="#91a4bc", font=font_normal).pack(
    anchor="w", padx=5
)
subject_entry = tk.Entry(
    email_frame,
    bg="#008744",
    fg="white",
    font=font_normal,
    width=50,
    insertbackground="white",
)
subject_entry.pack(fill="x", padx=5, pady=2)

tk.Label(email_frame, text="Email text:", bg="#91a4bc", font=font_normal).pack(
    anchor="w", padx=5
)
text_area = scrolledtext.ScrolledText(
    email_frame,
    bg="#008744",
    fg="white",
    height=8,
    font=font_normal,
    insertbackground="white",
)
text_area.pack(fill="x", padx=5, pady=2)

# فریم گیرندگان
receivers_frame = tk.LabelFrame(
    window, text="Recipients(one email per line)", bg="#91a4bc", font=font_normal
)
receivers_frame.pack(fill="x", padx=10, pady=5)

receivers_text = scrolledtext.ScrolledText(
    receivers_frame,
    bg="#008744",
    fg="white",
    height=5,
    font=font_normal,
    insertbackground="white",
)
receivers_text.pack(fill="x", padx=5, pady=2)

# دکمه‌ها
button_frame = tk.Frame(window)
button_frame.pack(pady=10)
button_frame.config(bg="#91a4bc")

send_btn = tk.Button(
    button_frame,
    text="Send email",
    command=send_emails,
    bg="#4CAF50",
    fg="white",
    font=("Tahoma", 12, "bold"),
    width=15,
)
send_btn.pack(side="left", padx=5)

clear_btn = tk.Button(
    button_frame, text="Delete", command=clear_fields, font=font_normal, width=10
)
clear_btn.pack(side="left", padx=5)

# لاگ
log_frame = tk.LabelFrame(window, text="Log sending", bg="#91a4bc", font=font_normal)
log_frame.pack(fill="both", expand=True, padx=10, pady=5)

log_area = scrolledtext.ScrolledText(
    log_frame,
    bg="#008744",
    fg="white",
    height=8,
    font=("Tahoma", 10),
    insertbackground="white",
)
log_area.pack(fill="both", expand=True, padx=5, pady=2)

# وضعیت
status_label = tk.Label(window, text="Ready", font=("Tahoma", 11), fg="green")
status_label.pack(pady=5)

# راهنمای پایین
help_label = tk.Label(
    window,
    text=" Use the App password for gamil.⚠️",
    font=("Tahoma", 10, "bold"),
    fg="gray",
)
help_label.pack(pady=5)

# اجرای برنامه
if __name__ == "__main__":
    window.mainloop()
