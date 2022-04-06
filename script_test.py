from telegram import sendTelegramMsg
import time

current_time = time.strftime("%H:%M:%S")
sendTelegramMsg("1726140050", f"Script run at {current_time}")