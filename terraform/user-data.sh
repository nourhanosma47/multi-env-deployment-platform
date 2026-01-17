#!/bin/bash

# Update system
apt-get update
apt-get upgrade -y

# Install Docker
apt-get install -y docker.io docker-compose
systemctl start docker
systemctl enable docker

# Add ubuntu user to docker group
usermod -aG docker ubuntu

# Install Git
apt-get install -y git

# Install AWS CLI
apt-get install -y awscli

# Create application directory
mkdir -p /opt/app
cd /opt/app

# Clone repository (you'll need to update this with your repo URL)
# git clone <your-repo-url> .

# Create docker-compose override for production
cat > docker-compose.override.yml <<EOF
version: '3.8'
services:
  backend:
    restart: always
    environment:
      - ENVIRONMENT=production
  frontend:
    restart: always
  postgres:
    restart: always
  redis:
    restart: always
EOF

# Note: Manual steps required:
# 1. Clone your repository
# 2. Run: docker-compose up -d
# 3. Configure environment variables

# Create a systemd service for auto-start
cat > /etc/systemd/system/devops-app.service <<EOF
[Unit]
Description=DevOps Platform Application
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/app
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
User=ubuntu

[Install]
WantedBy=multi-user.target
EOF

# Enable the service (will start after manual setup)
systemctl daemon-reload
# systemctl enable devops-app.service

echo "EC2 instance setup completed!"
echo "Manual steps required:"
echo "1. SSH into instance"
echo "2. Clone repository to /opt/app"
echo "3. Run: docker-compose up -d"
