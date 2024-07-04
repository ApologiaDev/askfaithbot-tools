
import os
import json
import logging

import boto3
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_aws.llms.bedrock import Bedrock
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from dotenv import load_dotenv


load_dotenv()


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=900,
    chunk_overlap=20,
    length_function=len
)


def get_bedrock_runtime(region_name, *args, **kwargs):
    return boto3.client(service_name='bedrock-runtime', region_name=region_name, *args, **kwargs)


def get_langchain_bedrock_llm(model_id, client, *args, **kwargs):
    return Bedrock(model_id=model_id, client=client, *args, **kwargs)


def lambda_handler(events, context):
    # get query
    logging.info(events)
    print(events)
    if isinstance(events['body'], dict):
        logging.info("dictionary")
        print("dictionary")
        query = events['body']
    else:
        logging.info("string")
        print("string")
        query = json.loads(events['body'])

    # get query question
    question = query['question']

    # retrieve config
    vectorstoredir = os.getenv('FAISS_CORPUS_DIR')
    llm_name = query.get('llm_name', 'mistral.mixtral-8x7b-instruct-v0:1')

    # getting an instance of LLM
    llm_config = query.get('llm_config', {
        "max_tokens": 4096,
        "temperature": 0.7,
        "top_p": 0.8
    })
    bedrock_runtime = get_bedrock_runtime('us-east-1')
    llm = get_langchain_bedrock_llm(llm_name, bedrock_runtime, config=llm_config)

    # loading the embedding model
    # the embedding model must be saved to EFS first
    embed_path = os.getenv('EMBED_PATH')
    print('Embedding path: {}'.format(embed_path))
    print(' Exists? {}'.format(os.path.exists(embed_path)))
    print(' Its parent directory exists? {}'.format(os.path.isdir(os.path.dirname(embed_path))))
    embeddings_model = HuggingFaceEmbeddings(model_name=embed_path)
    if embeddings_model.client.tokenizer.pad_token is None:
        embeddings_model.client.tokenizer.pad_token = embeddings_model.client.tokenizer.eos_token

    # loading vector database
    print('Loading vector database: {} (Exists? {})'.format(vectorstoredir, os.path.isdir(vectorstoredir)))
    db = FAISS.load_local(vectorstoredir, embeddings_model, allow_dangerous_deserialization=True)
    retriever = db.as_retriever()

    # getting the chain
    print('Making langchain')
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type='stuff', retriever=retriever, return_source_documents=True)

    # get the results
    results = qa({'query': question})
    print(results)

    # return
    return {'statusCode': 200, 'body': results}
