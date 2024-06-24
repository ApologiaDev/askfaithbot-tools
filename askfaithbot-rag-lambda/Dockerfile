FROM python:3.8

ADD . /code

WORKDIR /code

RUN apt-get update && \
  apt-get install -y \
  g++ \
  libc6 \
  gfortran \
  make \
  cmake \
  unzip \
  libcurl4-openssl-dev

RUN pip install -U pip
RUN pip install -r requirements.txt
RUN pip install awslambdaric boto3
RUN python -c "from langchain_community.embeddings.gpt4all import GPT4AllEmbeddings; embedding_model = GPT4AllEmbeddings(model_name='all-MiniLM-L6-v2.gguf2.f16.gguf')"

ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "main.lambda_handler" ]
