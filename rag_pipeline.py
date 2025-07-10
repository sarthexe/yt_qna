from youtube_transcript_api import YouTubeTranscriptApi,TranscriptsDisabled
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI , OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
import re
import os
from langchain_core.runnables import RunnableParallel,RunnableBranch,RunnableLambda,RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import openai

def extract_youtube_id(url):
    """
    Extract the video ID from a YouTube URL.
    Supports multiple YouTube URL formats.
    """
    regex = (
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    )
    match = re.search(regex, url)
    if match:
        return match.group(1)
    else:
        return None
    
def answer_question(api_key:str, video_url:str ,question:str)->str:
    
    os.environ['OPENAI_API_KEY']=api_key

    #data ingestion

    video_id = extract_youtube_id(url=video_url)
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id=video_id,languages=['en'])
        
        #flatter in to plain text
        transcript = ' '.join(chunk['text'] for chunk in transcript_list)
        print(transcript)

    except TranscriptsDisabled:
        print("No caption available for this video")

    #Data splitting

    splitter = RecursiveCharacterTextSplitter(chunk_size = 1000,chunk_overlap=200)
    chunks = splitter.create_documents([transcript])

    #Embedding gen and vectore storage
    
    embeddings = OpenAIEmbeddings(model = 'text-embedding-3-small')
    vector_store = FAISS.from_documents(chunks,embeddings)

    #retrieval
    retriever = vector_store.as_retriever(search_type='similarity',search_kwargs={'k':4})

    #augmentation
    llm = ChatOpenAI(model = "gpt-4o-mini",temperature = 0.2)
    prompt = PromptTemplate(
        template = """
        You are helpful assistant.
        Answer only from the provided transcript context.
        If the context is insufficient , just say you dont know.

        {context}
        Question : {question}
        Answer :
        """,
        input_variables = ['context','question']
    )

    retrieved_docs=retriever.invoke(question)

    def format_docs(retrieved_docs):
        context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
        return context_text

    parallel_chain = RunnableParallel({
        'context': retriever | RunnableLambda(format_docs),
        'question': RunnablePassthrough()
        })
    
    parser = StrOutputParser()

    main_chain = parallel_chain | prompt | llm | parser

    result = main_chain.invoke(question)

    return result
