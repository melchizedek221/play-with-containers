#!/bin/bash
set -e

echo "Script for Inventory app"

# Copie des fichiers de l'application
echo "Creating and copying all the files"
sudo mkdir -p opt/inventory-app
sudo cp -r /vagrant/srcs/inventory-app/* opt/inventory-app/
sudo cp /vagrant/.env opt/
sudo cp /vagrant/docker-compose.yaml opt/
echo "Done"

