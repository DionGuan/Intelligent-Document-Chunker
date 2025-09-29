# # 🧩 Intelligent Document Chunker

A lightweight knowledge base component for intelligent document segmentation using **semantic chunking techniques**.  
It supports both PDF and TXT inputs, performing structure-aware segmentation to enhance downstream knowledge retrieval and embedding quality.

---

## 📘 Introduction

**Intelligent Document Chunker** is designed to automatically divide long-form documents (`.txt` or `.pdf`) into smaller, semantically meaningful chunks.  
It integrates robust text extraction (via `OCR like MinerU`) with semantic embedding models (`sentence-transformers`) to produce content-aware document partitions ideal for LLM preprocessing, vector database ingestion, or knowledge base construction.

---

## ✨ Features

- ✅ Supports both **TXT** and **PDF** input formats  
- 🧠 Performs **semantic segmentation** using `sentence-transformers`  
- 📄 Extracts and cleans text from PDFs using **OCR like MinerU** (or compatible tools)  
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
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

> 💡 Tip:  
> It is strongly recommended to create and activate a virtual environment before installation:
> ```bash
> python -m venv .venv
> .venv\Scripts\activate    # Windows
> source .venv/bin/activate # macOS / Linux
> ```

---

### 3️⃣ Directory Structure

```bash
Chunk/
├── main.py
├── semantic_chunker_local.py
├── document_loader_local.py
├── test_file.pdf              # Example file for testing
└── output/                    # Automatically generated output
    └── test_file/
        ├── test_file.chunk.1.txt
        ├── test_file.chunk.2.txt
        ├── ...
        ├── test_file.all_chunks.txt
        └── auto/
            ├── test_file.md
            ├── test_file_content_list.json
            ├── test_file_layout.pdf
            ├── test_file_middle.json
            ├── test_file_model.json
            ├── test_file_origin.pdf
            ├── test_file_span.pdf
            └── images/         # OCR screenshots
                ├── img1.jpg
                ├── img2.jpg
                └── ...
```

---

### 4️⃣ Run the Application

Execute the following command in the terminal:

```bash
python main.py
```

You will be prompted to select a file path (TXT or PDF).  
The program will then automatically extract, clean, segment, and save the results under the `/output` directory.

---

## 🧩 Workflow Overview

```
TXT / PDF
   ↓
Text Extraction (OCR like MinerU for PDF)
   ↓
Markdown Cleaning
   ↓
Semantic Embedding & Chunk Detection
   ↓
Chunked Output Files (.txt)
```

---

## 🧠 Typical Use Cases

- Preprocessing large documents for **LLM training or fine-tuning**  
- Preparing content for **semantic search** or **vector databases** (e.g., FAISS, Milvus)  
- Structuring long documents for **knowledge retrieval systems**  
- Academic, legal, or technical **document analysis pipelines**

---

## ⭐ Todo List
- [x] OCR recognition optimization based on MinerU has been completed
- [ ] Implement more standardized preprocessing for `Markdown` and `JSON` files  
- [ ] Develop more detailed sliding window strategies tailored to the recognition of different document types.
- [ ] Integrate powerful Qwen3-embedding and Qwen3-reranker models to build a complete Retrieval-Augmented Generation (RAG) system.
- [ ] Integrate the system into an open-source AI platform.

---

## 🧪 Example Output (Terminal)

```
📂 Loading file: D:\...\test_file.pdf
🖼️  Parsing PDF using MinerU...
📄  Markdown file detected: output/test_file/auto/test_file.md
🧹  Markdown cleaning completed.
📖  Extracted and cleaned text length: 48,372 characters
✂️  Initializing semantic chunker...
✅  Local semantic chunker loaded: sentence-transformers/all-MiniLM-L6-v2
🧠  Performing semantic segmentation...
🎯  Completed — 42 chunks generated.
💾  Saving results...
✅  Output saved to: output/test_file/test_file.all_chunks.txt
```

---

## 📜 License

This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute this software, provided that the original copyright notice and this license are included in all copies or substantial portions of the Software.

> For more details, see the [LICENSE](./LICENSE) file.

---

## 🤝 Contributing

Contributions are welcome!  
If you’d like to improve functionality, fix bugs, or extend compatibility (e.g., support for other file types or embedding models), please feel free to open a pull request or create an issue.

---

## 📫 Contact

For questions or collaboration opportunities, please contact the project maintainer.

---

© 2025 Shenzhen Longgang District Data Co., Ltd. - Data Asset Management Center - Computational Modeling Department.
Developed for research and educational purposes.
# #
