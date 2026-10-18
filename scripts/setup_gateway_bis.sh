sudo apt-get install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install -y python3.8

# Set Python 3.8 as default
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
sudo update-alternatives --set python3 /usr/bin/python3.8

sudo apt-get install -y python3-pip libpq-dev python3-dev build-essential
sudo pip3 install flask requests pika python-dotenv flask-restx importlib-metadata