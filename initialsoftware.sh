# Install all of the core software needed to make use of a SDR (software defined radio)
# Based on instructions at https://www.rtl-sdr.com/video-tutorial-installing-gqrx-and-rtl-sdr-on-a-raspberry-pi/

# Start at the beginning by going home.
cd ~

# Make sure everything is up-to-date and then install core packages
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install python-pip
sudo pip install speedtest-cli
