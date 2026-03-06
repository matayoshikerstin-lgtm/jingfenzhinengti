import asyncio
import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

# 你的测试问题和结果保存的文件路径
EXCEL_PATH = 'test_result/result.xlsx'
# 你们内网经分智能体的地址
TARGET_URL = 'http://172.30.32.19:30016/home'

async def run_rpa_test():
    # 读取你要测的问题
    try:
        df = pd.read_excel(EXCEL_PATH)
    except Exception as e:
        print(f"读取Excel失败: {e}")
        return

    # 如果没有“智能体回复”这一列，就创建一个
    if '智能体回复' not in df.columns:
        df['智能体回复'] = ''

    print(f"成功加载题库，共 {len(df)} 道题。准备启动 Edge 浏览器...")

    async with async_playwright() as p:
        # channel='msedge' 表示强行使用你电脑里的 Microsoft Edge 浏览器
        # headless=False 表示不隐藏浏览器，你可以肉眼看着它怎么点
        browser = await p.chromium.launch(headless=False, channel="msedge")
        
        # 建立一个上下文，这里不使用隐身模式，尽量复用你的内网状态
        context = await browser.new_context()
        page = await context.new_page()

        print(f"正在打开网页: {TARGET_URL}")
        await page.goto(TARGET_URL)

        # ====== 【重点】人工登录缓冲时间 ======
        print("\n⏳ [请注意]：如果网页需要登录，请在这 15 秒内手动完成登录！如果已经登录，请等待...")
        await page.wait_for_timeout(15000)
        
        # 遍历每一道题
        for index, row in df.iterrows():
            question = str(row['问题'])
            if pd.isna(question) or question.strip() == "":
                continue
                
            # 如果这道题已经有回复了，跳过（支持断点续传）
            if pd.notna(row['智能体回复']) and str(row['智能体回复']).strip() != "":
                print(f"跳过已测题目: {question[:15]}...")
                continue

            print(f"\n[{index+1}/{len(df)}] 正在提问: {question}")

            try:
                # 1. 找到输入框（通常是 textarea 或者 input）
                # 这里使用你截图里的 placeholder 作为定位依据
                input_box = page.get_by_placeholder("输入您的业务指令")
                
                # 如果因为各种原因定位不到，尝试备用定位器
                if await input_box.count() == 0:
                    input_box = page.locator("textarea").last

                # 清空输入框并填入问题
                await input_box.fill("")
                await input_box.fill(question)
                
                # 2. 点击发送按钮
                # 根据你截图，是一个带有纸飞机图标的按钮
                # 你可以根据实际情况修改这里的定位，比如寻找 button 或者按回车
                await page.keyboard.press("Enter")
                
                # 3. 等待回复生成
                print("⏳ 等待智能体回复生成中 (预设等待 15 秒)...")
                # 这里根据你们大模型出字的速度调整。如果是流式的，需要等它出完。
                await page.wait_for_timeout(15000)
                
                # 4. 抓取回答
                # 这一步需要根据网页的 HTML 结构来定位。通常是 class 包含 message、bubble、content 等
                # 我们暂时假设抓取页面上最后一段长文本
                # 请根据实际页面 F12 检查到的 class 替换 '.message-content'
                responses = await page.locator("div.message-content, div.markdown-body").all_inner_texts()
                
                if responses:
                    # 取最后一条气泡作为回答
                    answer_text = responses[-1].strip()
                    print(f"✅ 获取到回答，长度: {len(answer_text)} 字符")
                    df.at[index, '智能体回复'] = answer_text
                else:
                    print("⚠️ 未能抓取到回答文字，请检查定位器配置。")
                    df.at[index, '智能体回复'] = "【自动化抓取失败】"
                
                # 实时保存 Excel，防止中途崩溃
                df.to_excel(EXCEL_PATH, index=False)

                # 5. 如果网页需要点击“新对话”按钮清除上下文，可以在这里加一步点击动作
                # await page.get_by_text("新对话").click()
                await page.wait_for_timeout(2000)

            except Exception as e:
                print(f"❌ 提问时发生错误: {e}")
                
        print("\n🎉 全部题目测试完毕！")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_rpa_test())
