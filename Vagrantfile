Vagrant.configure("2") do |config|
    config.vm.box = "ubuntu/bionic64"
    # config.vm.network "public_network", ip: "11.11.90.222", bridge: "en0: Wi-Fi"
    config.vm.network "public_network", ip: "192.168.1.90", bridge: "en0: Wi-Fi"
    config.vm.provision "shell", path: "scripts/install_docker.sh"
    config.vm.provision "shell", path: "scripts/setup_billing.sh"
    config.vm.provision "shell", path: "scripts/setup_gateway.sh"
    config.vm.provision "shell", path: "scripts/setup_inventory.sh"
    # config.vm.provision "shell", path: "scripts/run_docker.sh"
end
