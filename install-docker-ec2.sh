# 1. Update package list
sudo apt update

# 2. Install Docker
sudo apt install -y docker.io

# 3. Enable Docker to start on boot
sudo systemctl enable docker

# 4. Start Docker
sudo systemctl start docker

# 5. Add your user to the docker group (optional but recommended)
sudo usermod -aG docker ubuntu

# 6. Verify installation
docker --version
