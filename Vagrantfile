# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "mininet"

  #config.vm.network "public_network", :nat
  config.vm.network :private_network, ip: '172.16.10.3'
  config.vm.synced_folder '.', '/vagrant', nfs: true
  config.ssh.forward_agent = true

  config.vm.provider "virtualbox" do |v|
    v.name = "min"
    v.gui = false
  end
end
