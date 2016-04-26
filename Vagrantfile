# -*- mode: ruby -*-
# vi: set ft=ruby :

#
# Vagrant file for local provisioning
#
Vagrant::configure("2") do |config|

#  ansible_dir = "../madrid-infra/ansible"
#  ansible_verbose = "v"
#  shared_dir = "../"
  config.vm.box = "oinume/ubuntu-16.04"
  config.vm.hostname = "wdb93-sql"

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

  if Vagrant.has_plugin?("vagrant-cachier")
    config.cache.scope = :box
  end

  # Ansible
  # config.vm.provision :ansible do |ansible|
  #   ansible_dir = File.expand_path(ansible_dir)
  #   ansible.playbook = "#{ansible_dir}/local.yml"
  #   ansible.groups = {
  #     "local" => ["default"],
  #   }
  #   ansible.verbose = ansible_verbose
  # end

  # If you do not want to install ansible to local machine, Try this
  # config.vm.provision :shell do |shell|
  #   shell.inline = "cd /vagrant && sudo ./setup_ansible && sudo ansible-playbook provisioning/site.yml -i provisioning/localhost"
  # end

end
