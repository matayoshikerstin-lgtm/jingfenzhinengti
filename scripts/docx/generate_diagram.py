import asyncio
from playwright.async_api import async_playwright
import os

html_content = """
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
  <script>
    mermaid.initialize({
      startOnLoad: true,
      theme: 'default',
      securityLevel: 'loose'
    });
  </script>
  <style>
    body { background: white; margin: 20px; font-family: sans-serif; padding: 20px; }
    .mermaid { display: flex; justify-content: center; padding: 20px; background: white;}
  </style>
</head>
<body>
  <div class="mermaid" id="diagram">
graph TD
    classDef blue fill:#e1f5fe,stroke:#29b6f6,stroke-width:2px,color:#000;
    classDef green fill:#e8f5e9,stroke:#66bb6a,stroke-width:2px,color:#000;
    classDef orange fill:#fff3e0,stroke:#ffa726,stroke-width:2px,color:#000;
    classDef red fill:#ffebee,stroke:#ef5350,stroke-width:2px,color:#000;

    A[题库构建: 80道业务问题]:::blue --> B(RPA 自动化引擎):::orange
    B --> C[模拟人工登入内网]:::orange
    C --> D[逐题提问并抓取回复]:::orange
    D --> E{双轨智能交叉验证}:::blue
    
    E -->|非开放问题| F[脚本硬性比对: 正则提取 + Ground Truth]:::green
    E -->|开放问题| G[LLM裁判: 事实/洞察/建议 量化打分]:::green
    
    F --> H[判断准确率]:::green
    G --> I{分数 < 3 或 幻觉?}:::red
    
    I -->|Yes| J[触发人工兜底复检]:::red
    I -->|No| K[通过]:::green
    
    H --> L((输出高维可视化测试报告)):::blue
    J --> L
    K --> L
  </div>
</body>
</html>
"""

with open("temp_mermaid.html", "w", encoding="utf-8") as f:
    f.write(html_content)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        file_url = 'file:///' + os.path.abspath("temp_mermaid.html").replace('\\', '/')
        await page.goto(file_url)
        # Wait for mermaid to finish rendering
        await page.wait_for_selector("svg")
        await page.wait_for_timeout(1000) # give it a sec to finish drawing
        element = await page.query_selector("#diagram")
        await element.screenshot(path="test_plan/flowchart.png")
        await browser.close()
        print("Flowchart image generated at test_plan/flowchart.png")

asyncio.run(main())
