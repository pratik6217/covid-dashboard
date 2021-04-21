FROM ubuntu:latest
RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

COPY . ./ 
RUN pip3 install -r ./requirements.txt

EXPOSE 8501

CMD streamlit run main.py --server.maxUploadSize 1

