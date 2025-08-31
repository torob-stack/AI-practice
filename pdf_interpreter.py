import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate

# 🔑 Your API key here (local only, don’t share/commit this)
OPENAI_API_KEY = "openai_key"
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# 1) Load PDF replace with your own, I used the job description of the job I was applying for
loader = PyPDFLoader("job_description.pdf")
documents = loader.load()

# 2) Split into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = text_splitter.split_documents(documents)

# 3) Embed + store in Chroma
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(docs, embeddings)

# 4) Build retriever + custom prompt
retriever = vectorstore.as_retriever()

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=(
        "You are a helpful assistant.\n"
        "Use the provided context to answer the question.\n"
        "If the answer is not in the context, reply exactly: \"Not in the document.\"\n"
        "Respond ONLY with valid JSON using keys: answer, summary, sources.\n\n"
        "Context:\n{context}\n\n"
        "Question: {question}\n"
        "JSON:"
    ),
)

qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0),
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt},
)

# 5) Chat loop
print("📄 Document Chatbot Ready! Ask me questions (type 'quit' to exit).\n")
while True:
    query = input("You: ")
    if query.lower().strip() == "quit":
        break
    answer = qa.run(query)  # returns JSON as string
    print("Bot:", answer, "\n")
