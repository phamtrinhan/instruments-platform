
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add
sudo apt update
sudo apt install -y unzip xvfb libxi6 libgconf-2-4
sudo apt install -y default-jdk
sudo bash -c "echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google-chrome.list"
sudo apt -y update
sudo apt -y install google-chrome-stable


