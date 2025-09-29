# 🧩 Intelligent Document Chunker

A lightweight knowledge base component for intelligent document segmentation using **semantic chunking techniques**.  
It supports both PDF and TXT inputs, performing structure-aware segmentation to enhance downstream knowledge retrieval and embedding quality.

---

## 📘 Introduction

**Intelligent Document Chunker** is designed to automatically divide long-form documents (`.txt` or `.pdf`) into smaller, semantically meaningful chunks.  
It integrates robust text extraction (via `MinerU`) with semantic embedding models (`sentence-transformers`) to produce content-aware document partitions ideal for LLM preprocessing, vector database ingestion, or knowledge base construction.

---

## ✨ Features

- ✅ Supports both **TXT** and **PDF** input formats  
- 🧠 Performs **semantic segmentation** using `sentence-transformers`  
- 📄 Extracts and cleans text from PDFs using **MinerU** (or compatible tools)  
- 💾 Exports chunked text as individual `.txt` files and a combined summary file  
- 📂 Generates a structured output folder for easy downstream processing  

---

## ⚙️ Environment Requirements

- Python **3.8+**
- Recommended: Virtual environment for dependency isolation

---

## 🚀 Quick Start

### 1️⃣ Clone or Download the Repository

```bash
git clone <your-repo-url>
# or simply download and extract the project archive

💡 Tip:
It is strongly recommended to create and activate a virtual environment before installation:
python -m venv .venv
.venv\Scripts\activate    # Windows
source .venv/bin/activate # macOS / Linux

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
# 推荐使用虚拟环境进行部署，以隔离依赖

### 3️⃣ Directory Structure
```bash
   Chunk/
   ├── main.py
   ├── semantic_chunker_local.py
   ├── document_loader_local.py
   ├── test_file.pdf # 用以测试的文件
   └── output/ #生成的output文件夹
       └── test_file/
           ├── test_file.chunk.1.txt
           ├── test_file.chunk.2.txt
           ├── ...
           └── test_file.all_chunks.txt
           └── auto/
               ├── test_file.md
               ├── test_file_content_list.json
               ├── test_file_layout.pdf
               ├── test_file_middle.json
               ├── test_file_model.json
               ├── test_file_origin.pdf
               ├── test_file_span.pdf
               └── images/ #OCR 截图
                   ├── img1.jpg
                   ├── img2.jpg
                   └── ...

### 4️⃣ Run the Program
   ```bash
   python main.py

You will be prompted to select a document (either `.txt` or `.pdf`).
The system will automatically process the file, perform semantic segmentation, and save the results in the output directory.

# 📜 License
本项目仅用于研究与教学目的，可自由修改、复用与扩展。
