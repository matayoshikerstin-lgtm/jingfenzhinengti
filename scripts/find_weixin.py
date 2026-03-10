import uiautomation as auto

weixin = auto.WindowControl(searchDepth=1, Name='微信')
if not weixin.Exists(5):
    print("未找到微信窗口")
    exit()

def print_controls(ctrl, depth=0):
    indent = "  " * depth
    print(f"{indent}[{ctrl.ControlTypeName}] Name: {ctrl.Name!r}, ClassName: {ctrl.ClassName!r}")
    if depth < 8:
        for child in ctrl.GetChildren():
            print_controls(child, depth + 1)

print_controls(weixin)
