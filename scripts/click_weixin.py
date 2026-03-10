import uiautomation as auto

weixin = auto.WindowControl(searchDepth=1, Name='微信')
if not weixin.Exists(3):
    print("未找到微信窗口")
    exit()

# 找到"进入微信"按钮（XOutlineButton 类型）
btn = weixin.ButtonControl(ClassName='mmui::XOutlineButton')
if btn.Exists(3):
    print(f"找到按钮，正在点击...")
    btn.SetFocus()
    btn.Click(simulateMove=True)
    print("点击成功！")
else:
    print("未找到进入微信按钮")
