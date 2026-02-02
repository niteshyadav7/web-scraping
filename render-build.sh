#!/usr/bin/env bash
# Render.com build script - Backend only

echo "🚀 Starting backend build..."

# Install Chrome dependencies
echo "📦 Installing Chrome dependencies..."
apt-get update
apt-get install -y wget gnupg unzip

# Install Chrome
echo "🌐 Installing Google Chrome..."
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
apt-get update
apt-get install -y google-chrome-stable

# Install ChromeDriver
echo "🚗 Installing ChromeDriver..."
CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget -N https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip -P ~/
unzip ~/chromedriver_linux64.zip -d ~/
rm ~/chromedriver_linux64.zip
mv -f ~/chromedriver /usr/local/bin/chromedriver
chmod +x /usr/local/bin/chromedriver

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install -r requirements.txt

echo "✅ Backend build complete!"
