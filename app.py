import streamlit as st
import os
import tempfile
from rag_engine import load_document, build_rag_chain

# 页面配置（只运行一次）
st.set_page_config(
    page_title="企业内部文档智能助手",
    page_icon="📚",
    layout="wide"
)

# 初始化会话状态（保存页面刷新不丢失）
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_file" not in st.session_state:
    st.session_state.current_file = None

# 侧边栏：文档上传区域
with st.sidebar:
    st.header("📁 知识库管理")
    uploaded_file = st.file_uploader(
        "上传企业文档", 
        type=["pdf", "docx", "txt", "md"],
        help="支持PDF、Word、TXT、Markdown格式"
    )
    
    # 当用户上传了新文件
    if uploaded_file is not None:
        if st.session_state.current_file != uploaded_file.name:
            with st.spinner("正在解析文档并构建知识库..."):
                # 保存为临时文件
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                
                # 加载文档并构建RAG链
                documents = load_document(tmp_path)
                st.session_state.rag_chain, _ = build_rag_chain(documents)
                st.session_state.current_file = uploaded_file.name
                st.session_state.chat_history = []  # 清空历史对话
                
                # 删除临时文件
                os.unlink(tmp_path)
                
                st.success(f"✅ 知识库构建完成！\n文档：{uploaded_file.name}")
    
    st.markdown("---")
    st.subheader("📊 系统信息")
    st.write(f"当前文档：{st.session_state.current_file or '无'}")
    st.write(f"对话历史：{len(st.session_state.chat_history)}条")
    
    if st.button("清空对话历史"):
        st.session_state.chat_history = []
        st.rerun()

# 主界面：聊天区域
st.title("🏢 企业内部文档智能问答助手")
st.markdown("上传企业文档后，即可用自然语言提问获取精准答案")

# 显示历史对话
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 用户输入框
if prompt := st.chat_input("请输入你的问题..."):
    if st.session_state.rag_chain is None:
        st.warning("⚠️ 请先在左侧上传文档构建知识库")
    else:
        # 添加用户消息到历史
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # 生成回答
        with st.chat_message("assistant"):
            with st.spinner("正在思考..."):
                response = st.session_state.rag_chain.invoke(prompt)
                st.markdown(response)
        
        # 添加助手回答到历史
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()