import streamlit as st
import pandas as pd
import os
from pathlib import Path

# 配置页面
st.set_page_config(page_title="经分智能体 - LLM裁判复核系统", layout="wide")
st.title("🤖 经分智能体 - LLM裁判人工复核系统")
st.markdown("此工具用于人工抽检和复核 LLM 裁判的打分结果，以优化裁判 Prompt 和评估真实效果。")

# 确定数据文件路径
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent.parent
data_file = project_root / 'test_result' / 'result.xlsx'

# 初始化 session state 用于分页和数据管理
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0

@st.cache_data
def load_data(file_path):
    if not os.path.exists(file_path):
        # 如果文件不存在，创建一个模拟的空 DataFrame 以作演示
        return pd.DataFrame({
            "问题": ["示例问题：本月收入环比增长多少？"],
            "智能体回复": ["本月收入环比增长了5.2%"],
            "标准答案": ["本月收入环比增长5.2%"],
            "LLM裁判得分": [1.0],
            "人工复核得分": [None],
            "人工复核备注": [""]
        })
    df = pd.read_excel(file_path)
    # 确保人工复核列存在
    if '人工复核得分' not in df.columns:
        df['人工复核得分'] = None
    if '人工复核备注' not in df.columns:
        df['人工复核备注'] = ""
    return df

def save_data(df, file_path):
    if os.path.exists(file_path):
        df.to_excel(file_path, index=False)
        st.success("✅ 数据已成功保存回 result.xlsx！")
    else:
        st.warning("⚠️ 找不到真实的 result.xlsx，演示数据未保存。请确保 RPA 脚本已生成测试结果。")

# 加载数据
df = load_data(data_file)
total_records = len(df)

if total_records == 0:
    st.info("数据集中没有记录。")
    st.stop()

# 侧边栏导航和保存
with st.sidebar:
    st.header("导航与操作")
    st.write(f"当前进度：{st.session_state.current_index + 1} / {total_records}")
    
    # 进度条
    progress = (st.session_state.current_index + 1) / total_records
    st.progress(progress)
    
    # 导航按钮
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ 上一条", disabled=st.session_state.current_index == 0):
            st.session_state.current_index -= 1
            st.rerun()
    with col2:
        if st.button("下一条 ➡️", disabled=st.session_state.current_index == total_records - 1):
            st.session_state.current_index += 1
            st.rerun()
            
    st.divider()
    
    if st.button("💾 保存所有修改", type="primary", use_container_width=True):
        save_data(df, data_file)

# 主体内容展示区
current_record = df.iloc[st.session_state.current_index]

# 展示原始数据
st.subheader("📝 测试用例详情")
col_q, col_a = st.columns(2)
with col_q:
    st.markdown("**🔍 用户问题：**")
    st.info(current_record.get('问题', '无数据'))
    st.markdown("**🎯 标准答案（Ground Truth）：**")
    st.success(current_record.get('标准答案', '无数据'))
    
with col_a:
    st.markdown("**🤖 智能体回复：**")
    st.warning(current_record.get('智能体回复', '无数据'))
    st.markdown("**⚖️ LLM 裁判原始得分：**")
    llm_score = current_record.get('LLM裁判得分', '未打分')
    if pd.isna(llm_score): llm_score = '未打分'
    st.metric(label="LLM 裁判打分", value=llm_score)

st.divider()

# 人工复核操作区
st.subheader("🕵️ 人工复核 (Human-in-the-loop)")

# 获取当前的人工复核值（如果有）
current_human_score = current_record.get('人工复核得分')
current_human_remark = current_record.get('人工复核备注')
if pd.isna(current_human_remark): current_human_remark = ""

col_score, col_remark = st.columns([1, 2])

with col_score:
    # 预设的打分选项：完全一致(1.0)，部分一致(0.5)，不一致(0.0)
    score_options = [1.0, 0.5, 0.0]
    # 确定默认选项索引
    default_index = 0
    if not pd.isna(current_human_score) and current_human_score in score_options:
        default_index = score_options.index(current_human_score)
    elif not pd.isna(llm_score) and llm_score in score_options:
        # 如果还没人工复核，默认选中LLM的打分作为参考
        default_index = score_options.index(llm_score)

    new_score = st.radio(
        "人工校准打分：",
        options=score_options,
        index=default_index,
        format_func=lambda x: f"{x} 分" + (" (完全一致)" if x==1.0 else " (部分一致)" if x==0.5 else " (不一致)"),
        horizontal=True
    )

with col_remark:
    new_remark = st.text_input("复核备注（如裁判为何打错等）：", value=current_human_remark)

# 自动提交当前页更改到 DataFrame
if new_score != current_human_score or new_remark != current_human_remark:
    df.at[st.session_state.current_index, '人工复核得分'] = new_score
    df.at[st.session_state.current_index, '人工复核备注'] = new_remark
    # 不需要立即持久化到硬盘，等用户点左侧的"保存所有修改"

st.markdown("---")
st.caption("提示：修改打分和备注后会自动暂存在内存中，请务必点击左侧边栏的 **保存所有修改** 按钮将结果写入 Excel 文件。")
