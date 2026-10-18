#!/bin/bash
set -e

echo "Script for Billing app"

# Copie des fichiers de l'application
sudo mkdir -p opt/billing-app
sudo cp -r /vagrant/srcs/billing-app/* opt/billing-app/
