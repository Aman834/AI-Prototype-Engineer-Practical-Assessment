from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()


def create_rag_pipeline(chunks):
    # 1. Create embeddings
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    # 2. Store embeddings in FAISS
    vector_store = FAISS.from_documents(chunks, embeddings)

    # 3. Create retriever
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})

    # 4. Initialize LLM
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0
    )

    # 5. Return a callable QA function (modern RAG)
    def qa_function(question: str):
        # Retrieve relevant chunks
        docs = retriever.get_relevant_documents(question)

        if not docs:
            return {
                "result": "I don't know based on the provided document.",
                "source_documents": []
            }

        # Build context
        context = "\n\n".join(doc.page_content for doc in docs)

        system_prompt = (
            "You are an assistant that answers questions ONLY using the provided context.\n"
            "If the answer is not in the context, say: "
            "'I don't know based on the provided document.'"
        )

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(
                content=f"Context:\n{context}\n\nQuestion:\n{question}"
            )
        ]

        response = llm.invoke(messages)

        return {
            "result": response.content,
            "source_documents": docs
        }

    return qa_function
