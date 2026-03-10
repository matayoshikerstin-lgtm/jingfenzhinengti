import pyautogui
import time

# 截图保存，用于查看当前微信界面
screenshot = pyautogui.screenshot()
screenshot.save("d:/jfznt/仓库/jingfenzhinengti/scripts/weixin_screen.png")
print("截图已保存")
