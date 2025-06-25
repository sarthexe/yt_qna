
# 📽️ YouTube Video Q&A using RAG + Gradio

This project allows users to ask questions about the content of any YouTube video. It uses **Retrieval-Augmented Generation (RAG)** to process the video transcript and answer questions via a **Gradio web interface**.

---

## 🚀 Features

- 🔍 Extracts transcript from YouTube videos
- 🧠 Retrieves relevant content using embeddings
- 💬 Answers questions using an LLM
- 🌐 Interactive UI with Gradio
- 📎 Supports multiple YouTube URL formats

---

## 🔧 How It Works

1. **Input**: User provides a YouTube URL and a question.
2. **Transcript**: The video transcript is extracted via `youtube-transcript-api`.
3. **Chunking + Embedding**: Transcript is chunked and embedded using Sentence Transformers.
4. **Retrieval**: Relevant chunks are retrieved via vector similarity (e.g., FAISS).
5. **Generation**: A language model (e.g., GPT) generates an answer based on the context.
6. **Output**: Answer is displayed in the Gradio UI.

---

## 🛠️ Technologies Used

- Python 🐍
- [Gradio](https://www.gradio.app/)
- OpenAI Chat Model
- OpenAI Embeddings
- [YouTube Transcript API](https://pypi.org/project/youtube-transcript-api/)
- FAISS (or in-memory retrieval)

---

## 🖥️ Usage

### 🔗 1. Clone the repository

```bash
git clone https://github.com/sarthexe/yt_qna
cd yt_qna
```
### 📦 2. Install dependencies
```bash
pip install -r requirements.txt
```
### ▶️ 3. Run the app
```bash
python main.py
```

The app will launch in your browser. You can also set share=True in gr.Interface(...).launch() to get a public link.

| Input                                            | Output                                        |
| ------------------------------------------------ | --------------------------------------------- |
| YouTube URL: `https://youtu.be/dQw4w9WgXcQ`      |                                               |
| Question: `What is the main topic of the video?` | A detailed answer based on transcript content |




## Authors

### Sarthak Kumar Maurya

Feel free to open an issue or pull request for improvements!

