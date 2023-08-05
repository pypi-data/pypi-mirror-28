#!/bin/bash
echo '*** executing script ***'
sudo apt-get update
sudo apt-get --assume-yes install {}
sudo apt-get install unzip
sudo ln -s /usr/bin/{} /usr/bin/python
cd /tmp		
wget https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/debian_amd64/amazon-ssm-agent.deb
sudo dpkg -i amazon-ssm-agent.deb
sudo systemctl enable amazon-ssm-agent
echo 'finished executing'