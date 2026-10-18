FROM python:3.12-alpine

WORKDIR /usr/src/

COPY requirements.txt ./

# RUN pip install --no-cache-dir -r requirements.txt
RUN pip3 install flask requests pika python-dotenv flask-restx importlib-metadata

# COPY setup_gateway_bis.sh ./
# RUN chmod +x setup_gateway_bis.sh
# RUN ./setup_gateway_bis.sh

# RUN apt-get update && apt-get install -y software-properties-common \
#     && add-apt-repository ppa:deadsnakes/ppa \
#     && apt-get update \
#     && apt-get install -y python3.8 python3-pip libpq-dev python3-dev build-essential \
#     && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1 \
#     && update-alternatives --set python3 /usr/bin/python3.8

EXPOSE 3000

COPY . .

CMD ["python3", "server.py"]