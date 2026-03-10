"""
监控 hello_claude.txt 文件变化，有更新时打印内容并弹出 Windows 通知
"""
import sys
import time
import os
import subprocess

# 强制 stdout 使用 UTF-8，避免 Windows GBK 终端无法打印 emoji
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "hello_claude.txt")

def notify(title, message):
    """Windows 气泡通知（通过 PowerShell）"""
    ps_script = f"""
Add-Type -AssemblyName System.Windows.Forms
$notify = New-Object System.Windows.Forms.NotifyIcon
$notify.Icon = [System.Drawing.SystemIcons]::Information
$notify.Visible = $true
$notify.ShowBalloonTip(5000, '{title}', '{message}', [System.Windows.Forms.ToolTipIcon]::Info)
Start-Sleep -Seconds 6
$notify.Dispose()
"""
    subprocess.Popen(["powershell", "-WindowStyle", "Hidden", "-Command", ps_script])

def read_file():
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        return f.read()

def main():
    print(f"开始监控: {FILE_PATH}")
    print("=" * 50)

    last_content = read_file()
    last_mtime = os.path.getmtime(FILE_PATH)

    print("当前内容：")
    print(last_content)
    print("=" * 50)
    print("等待文件变化...\n")

    while True:
        time.sleep(1)
        try:
            mtime = os.path.getmtime(FILE_PATH)
            if mtime != last_mtime:
                new_content = read_file()
                if new_content != last_content:
                    print("\n" + "=" * 50)
                    print(">>> 文件已更新！最新内容：")
                    print("=" * 50)
                    print(new_content)
                    print("=" * 50 + "\n")

                    # 找出新增的行
                    old_lines = set(last_content.splitlines())
                    new_lines = [l for l in new_content.splitlines() if l.strip() and l not in old_lines]
                    preview = new_lines[0][:50] if new_lines else "内容有变化"
                    notify("hello_claude.txt 有新消息", preview)

                    last_content = new_content
                last_mtime = mtime
        except Exception as e:
            print(f"读取出错: {e}")

if __name__ == "__main__":
    main()
