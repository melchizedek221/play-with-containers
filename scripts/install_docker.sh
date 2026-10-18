# #!/bin/bash

# echo "Updating packages..."
# sudo apt-get update -y

# echo "Installing dependencies..."
# sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# echo "Adding Docker's GPG key..."
# curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# echo "Adding Docker repository..."
# sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# echo "Updating packages after adding Docker repository..."
# sudo apt-get update -y

# # Install Docker
# echo "Installing Docker..."
# sudo apt-get install -y docker-ce

# # Check Docker installation
# echo "Checking Docker installation..."
# sudo systemctl status docker

# # Install Docker Compose
# echo "Installing Docker Compose..."
# DOCKER_COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")')
# sudo curl -L "https://github.com/docker/compose/releases/download/$DOCKER_COMPOSE_VERSION/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# sudo chmod +x /usr/local/bin/docker-compose

# # Check Docker Compose installation
# echo "Checking Docker Compose installation..."
# docker-compose --version

# echo "Adding the current user to the Docker group..."
# sudo usermod -aG docker vagrant

# # Display a completion message
# # echo "Installation completed. You need to log out and log back in for the changes to take effect."

#!/bin/bash
set -e

echo "Updating packages..."
sudo apt-get update -y

echo "Installing dependencies..."
sudo apt-get install -y ca-certificates curl gnupg lsb-release

echo "Adding Docker's official GPG key..."
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo "Adding Docker repository..."
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

echo "Updating packages after adding Docker repository..."
sudo apt-get update -y

# Install Docker Engine + CLI + containerd + Buildx + Compose plugin
echo "Installing Docker..."
sudo apt-get install -y \
  docker-ce \
  docker-ce-cli \
  containerd.io \
  docker-buildx-plugin \
  docker-compose-plugin

# Check Docker installation
echo "Checking Docker installation..."
sudo systemctl enable docker
sudo systemctl status docker --no-pager

# Check Docker Compose (v2 plugin) installation
echo "Checking Docker Compose installation..."
docker compose version

# Check Buildx installation
echo "Checking Docker Buildx installation..."
docker buildx version

echo "Adding the current user to the Docker group..."
sudo usermod -aG docker vagrant

echo "Installation completed. You need to log out and log back in (or run 'newgrp docker') for the group changes to take effect."