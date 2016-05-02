# -*- mode: ruby -*-

Vagrant::configure("2") do |config|

  config.vm.box = "oinume/ubuntu-14.04-jp"
  config.vm.hostname = "wdb93-sql"
  #config.vm.synced_folder "./", "/tinyblog"

  # MySQL
  # config.vm.network :forwarded_port, guest: 3306, host: 23306
  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  config.vm.network :private_network, ip: "192.168.9.10"

  # VM option
  config.vm.provider "virtualbox" do |v|
    v.customize ["modifyvm", :id, "--memory", 512]
    v.customize ["modifyvm", :id, "--cpus", 1]
    v.customize ["modifyvm", :id, "--nictype1", "virtio"]
    v.customize ["modifyvm", :id, "--nictype2", "virtio"]
    v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
  end

  config.vm.provision :shell do |shell|
    shell.inline = "cd /vagrant && sh provision.sh"
  end

end
