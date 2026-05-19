# 企业级私有化RAG智能问答系统
本项目基于本地大模型搭建离线文档问答平台，无需调用任何云端API，实现企业内部PDF、Word、TXT文档智能检索问答，保障数据本地安全，适合企业知识库、产品手册、年报资料快速查询。

## 项目优势
1. 完全本地私有化部署，断网也能运行，无数据外泄风险
2. 使用通义千问Qwen2-7B量化模型，适配RTX3060 6G显存流畅运行
3. 采用BGE-M3中文嵌入模型 + FAISS高速向量库，检索速度快
4. 严格依据文档内容作答，杜绝大模型编造幻觉
5. 基于Streamlit搭建简洁网页交互界面，上手即用

## 技术栈
Python、LangChain、Ollama、Qwen2本地大模型、FAISS向量库、Streamlit
文档解析：PyPDF、python-docx

## 运行环境
1. 安装Ollama本地大模型工具
2. 拉取所需模型
ollama pull qwen2:7b-instruct-q4_0
ollama pull bge-m3

3. 安装项目依赖
pip install streamlit langchain langchain-ollama langchain-community faiss-cpu pypdf python-docx

## 启动运行
streamlit run app.py

## 使用方法
1. 浏览器自动打开本地网页 8501端口
2. 上传企业年报、产品手册、规章制度等文档
3. 等待自动分片构建向量知识库
4. 输入问题即可精准问答文档内容

## 适用场景
企业内部资料查询、汽车产品手册问答、上市公司年报数据分析、学习资料知识库问答
