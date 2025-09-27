import gradio as gr
import requests

API_URL = "http://api:8000/rag/ask"

def chat_fn(question: str):
    resp = requests.post(API_URL, json={"question": question, "top_k": 5}).json()
    answer = resp.get("answer", "")
    src = "\n".join([f"- {s['title']} (score={s['score']:.2f})" for s in resp.get("sources", [])])
    return f"{answer}\n\nSources\n{src}"

def main():
    gr.Interface(
        fn=chat_fn,
        inputs=gr.Textbox(label="Poser une question sur des articles arXiv"),
        outputs=gr.Markdown(),
        title="RAG — Curateur arXiv",
    ).launch(server_name="0.0.0.0", server_port=7861)

if __name__ == "__main__":
    main()
