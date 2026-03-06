import os
import glob
import json
from pathlib import Path

def export_latest_chat():
    # Cursor 存放聊天记录的目录 (根据你的环境)
    transcript_dir = r"C:\Users\blwang16\.cursor\projects\d-jfznt-jingfenzhinengti\agent-transcripts"
    
    # 获取所有的 jsonl 文件
    search_pattern = os.path.join(transcript_dir, "**", "*.jsonl")
    files = glob.glob(search_pattern, recursive=True)
    
    # 过滤掉 subagents 的记录，只看主对话
    main_files = [f for f in files if "subagents" not in f]
    
    if not main_files:
        print("未找到聊天记录文件。")
        return

    # 按修改时间排序，找到最新的一份聊天记录（通常就是当前的这个）
    latest_file = max(main_files, key=os.path.getmtime)
    print(f"正在读取最新的聊天记录: {latest_file}")
    
    output_md_path = r"d:\jfznt\仓库\jingfenzhinengti\与AI协作全过程.md"
    
    with open(latest_file, 'r', encoding='utf-8') as f_in, open(output_md_path, 'w', encoding='utf-8') as f_out:
        f_out.write("# 🤖 经分智能体测试方案：人机协作全过程记录\n\n")
        f_out.write("> **说明**：本文档由 Python 脚本自动抓取 Cursor 底层日志生成，完整还原了测试工程师与 AI 探讨、推翻、重建测试方案的真实对话流。\n\n---\n\n")
        
        for line in f_in:
            try:
                data = json.loads(line)
                role = data.get('role', '')
                
                # 提取文本内容
                text_content = ""
                if 'message' in data and 'content' in data['message']:
                    content_list = data['message']['content']
                    if isinstance(content_list, list):
                        for item in content_list:
                            if item.get('type') == 'text':
                                text_content += item.get('text', '')
                    elif isinstance(content_list, str):
                        text_content = content_list
                
                if not text_content:
                    continue
                    
                # 清洗一下 user_query 标签
                text_content = text_content.replace("<user_query>\n", "").replace("\n</user_query>", "").replace("<user_query>", "").replace("</user_query>", "")
                
                if role == 'user':
                    f_out.write(f"### 🧑‍💻 测试工程师 (User)\n\n{text_content.strip()}\n\n---\n\n")
                elif role == 'assistant':
                    # 如果 AI 回复太长（包含大量代码），可以选择性折叠，这里直接全量输出
                    f_out.write(f"### 🤖 AI 智能体 (Assistant)\n\n{text_content.strip()}\n\n---\n\n")
            except json.JSONDecodeError:
                continue

    print(f"Success! Chat exported to: {output_md_path}")
    print("Now you can copy and paste it to Feishu.")

if __name__ == "__main__":
    export_latest_chat()
