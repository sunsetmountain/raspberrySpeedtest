# Install all of the core software needed to perform repeated internet speed tests using a Raspberry Pi

# Start at the beginning by going home.
cd ~

# Make sure everything is up-to-date and then install core packages
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install python-pip
sudo pip install speedtest-cli
sudo pip install tendo
