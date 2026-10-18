#!/bin/bash
set -e
echo "Script for Api Gateway"

# Copie des fichiers de l'application
sudo mkdir -p opt/api-gateway
sudo cp -r /vagrant/srcs/api-gateway/* opt/api-gateway/
sudo cp -r /vagrant/scripts/setup_gateway_bis.sh opt/api-gateway/
