import ctypes
import ctypes.wintypes
import pyautogui
import time

user32 = ctypes.windll.user32

# 枚举所有窗口找微信
def find_weixin():
    result = []
    def callback(hwnd, _):
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buf = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buf, length + 1)
                name = buf.value
                if '微信' in name or 'WeChat' in name or 'Weixin' in name:
                    result.append((hwnd, name))
        return True
    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
    user32.EnumWindows(WNDENUMPROC(callback), 0)
    return result

windows = find_weixin()
print(f"找到微信窗口: {windows}")

if not windows:
    print("未找到")
    exit()

hwnd = windows[0][0]

# 恢复并置顶
SW_RESTORE = 9
user32.ShowWindow(hwnd, SW_RESTORE)
user32.SetForegroundWindow(hwnd)
time.sleep(1)

# 获取窗口位置
rect = ctypes.wintypes.RECT()
user32.GetWindowRect(hwnd, ctypes.byref(rect))
print(f"窗口位置: left={rect.left}, top={rect.top}, right={rect.right}, bottom={rect.bottom}")

# 点击文件传输助手（聊天列表第一项）
x = rect.left + 80
y = rect.top + 65
print(f"点击坐标: ({x}, {y})")
pyautogui.click(x, y)
time.sleep(0.5)

# 截图确认
screenshot = pyautogui.screenshot()
screenshot.save("d:/jfznt/仓库/jingfenzhinengti/scripts/weixin_screen.png")
print("完成")
