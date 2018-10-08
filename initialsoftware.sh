# Install all of the core software needed to perform repeated internet speed tests using a Raspberry Pi

# Start at the beginning by going home.
cd ~

# Make sure everything is up-to-date and then install core packages
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install python-pip
sudo pip install speedtest-cli
sudo pip install tendo

# Install Google Cloud packages
sudo pip install --upgrade google-cloud-storage
sudo pip install --upgrade google-cloud-pubsub
sudo pip install --upgrade oauth2client

# Create a data directory
cd ~/raspberrySpeedtest
mkdir speedtestResults

# Add startup commands to the end of .profile
echo "# export GOOGLE_APPLICATION_CREDENTIALS='/home/pi/FILENAME.json'"
echo "python /home/pi/raspberrySpeedtest/checkSpeed.py &" >> /home/pi/.profile
echo "# python /home/pi/raspberrySpeedtest/batchGCS.py &" >> /home/pi/.profile
