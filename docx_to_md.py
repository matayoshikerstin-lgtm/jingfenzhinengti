import os
import sys
import mammoth   #type ignore
from markdownify import markdownify as md  #type ignore

def convert_docx_to_md(docx_path, output_path=None):
    """
    将单个 docx 文件转换为 md 文件
    """
    if not os.path.exists(docx_path):
        print(f"错误: 文件不存在 - {docx_path}")
        return

    # 如果没有指定输出路径，默认在同目录下生成同名 md 文件
    if output_path is None:
        output_path = os.path.splitext(docx_path)[0] + ".md"

    print(f"正在转换: {docx_path} -> {output_path}")

    try:
        with open(docx_path, "rb") as docx_file:
            # 1. 使用 mammoth 将 docx 转换为 HTML
            # style_map 可以自定义样式映射，这里使用默认
            result = mammoth.convert_to_html(docx_file)
            html = result.value
            messages = result.messages # 警告信息

            # 打印警告信息（如果有）
            for message in messages:
                print(f"  [警告] {message}")

        # 2. 使用 markdownify 将 HTML 转换为 Markdown
        # heading_style="ATX" 使用 # 标题格式而不是下划线格式
        markdown_text = md(html, heading_style="ATX")

        # 3. 写入文件
        with open(output_path, "w", encoding="utf-8") as md_file:
            md_file.write(markdown_text)
        
        print("转换成功！")

    except Exception as e:
        print(f"转换失败: {e}")

def batch_convert(directory):
    """
    批量转换目录下的所有 docx 文件
    """
    if not os.path.exists(directory):
        print(f"错误: 目录不存在 - {directory}")
        return

    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".docx") and not file.startswith("~$"):
                full_path = os.path.join(root, file)
                convert_docx_to_md(full_path)
                count += 1
    
    print(f"\n批量处理完成，共转换 {count} 个文件。")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  转换单个文件: python docx_to_md.py <文件路径.docx>")
        print("  批量转换目录: python docx_to_md.py <文件夹路径>")
    else:
        target = sys.argv[1]
        if os.path.isfile(target):
            convert_docx_to_md(target)
        elif os.path.isdir(target):
            batch_convert(target)
        else:
            print("无效的路径")
