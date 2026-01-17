# Ansible Configuration Management

Ansible playbooks for automated deployment and configuration of the DevOps platform.

## 📋 Prerequisites

- Ansible 2.10+
- SSH access to target servers
- Python 3.x on target servers

## 📁 Directory Structure

```
ansible/
├── inventory/
│   └── hosts.yml          # Server inventory
├── playbooks/
│   ├── setup.yml          # Server setup playbook
│   └── deploy.yml         # Application deployment playbook
├── templates/
│   └── .env.j2            # Environment configuration template
├── ansible.cfg            # Ansible configuration
└── README.md              # This file
```

## 🚀 Usage

### 1. Install Ansible

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install ansible -y

# macOS
brew install ansible
```

### 2. Update Inventory

Edit `inventory/hosts.yml` and update:
- Server IP addresses
- SSH key paths
- Environment names

### 3. Test Connection

```bash
# Test all servers
ansible all -m ping

# Test specific environment
ansible development -m ping
ansible staging -m ping
ansible production -m ping
```

### 4. Server Setup (First Time)

```bash
# Setup development environment
ansible-playbook playbooks/setup.yml --limit development

# Setup staging
ansible-playbook playbooks/setup.yml --limit staging

# Setup production
ansible-playbook playbooks/setup.yml --limit production
```

### 5. Deploy Application

```bash
# Deploy to development
ansible-playbook playbooks/deploy.yml --limit development

# Deploy to staging
ansible-playbook playbooks/deploy.yml --limit staging

# Deploy to production
ansible-playbook playbooks/deploy.yml --limit production
```

## 📝 Playbook Details

### setup.yml - Server Setup

This playbook:
- Updates system packages
- Installs essential tools
- Configures firewall (UFW)
- Sets up Docker and Docker Compose
- Creates swap file
- Configures system limits
- Sets up log rotation
- Installs monitoring tools

**Usage:**
```bash
ansible-playbook playbooks/setup.yml
```

### deploy.yml - Application Deployment

This playbook:
- Clones/updates Git repository
- Builds Docker images
- Deploys containers with Docker Compose
- Performs health checks
- Verifies deployment

**Usage:**
```bash
ansible-playbook playbooks/deploy.yml
```

## 🎯 Common Tasks

### Deploy to specific environment

```bash
ansible-playbook playbooks/deploy.yml --limit production
```

### Run specific tags only

```bash
# Only setup Docker
ansible-playbook playbooks/setup.yml --tags docker

# Only deploy application
ansible-playbook playbooks/deploy.yml --tags deploy

# Only verify deployment
ansible-playbook playbooks/deploy.yml --tags verify
```

### Dry run (check mode)

```bash
ansible-playbook playbooks/deploy.yml --check
```

### Verbose output

```bash
ansible-playbook playbooks/deploy.yml -vvv
```

## 🔧 Configuration

### Environment Variables

Edit `templates/.env.j2` to customize:
- Database credentials
- Redis configuration
- Application settings
- Security keys

### Inventory Variables

In `inventory/hosts.yml`, you can set:
- `ansible_host`: Server IP/hostname
- `ansible_user`: SSH user
- `ansible_ssh_private_key_file`: SSH key path
- `environment`: Environment name (dev/staging/prod)

## 🧪 Testing

### Test playbook syntax

```bash
ansible-playbook playbooks/deploy.yml --syntax-check
```

### List all hosts

```bash
ansible all --list-hosts
```

### List all tasks

```bash
ansible-playbook playbooks/deploy.yml --list-tasks
```

## 📊 Monitoring

After setup, you can access:
- **Netdata**: http://SERVER_IP:19999 (if installed)

## 🔐 Security Best Practices

1. **Never commit sensitive data**:
   - SSH private keys
   - Passwords in inventory
   - API tokens

2. **Use Ansible Vault** for secrets:
   ```bash
   ansible-vault encrypt inventory/secrets.yml
   ansible-playbook playbooks/deploy.yml --ask-vault-pass
   ```

3. **Limit SSH access**:
   - Use key-based authentication only
   - Disable password authentication
   - Restrict source IPs in firewall

## 🐛 Troubleshooting

### Issue: Connection timeout

```bash
# Test SSH connection
ssh -i ~/.ssh/devops-key.pem ubuntu@SERVER_IP

# Check if port 22 is open
ansible all -m ping -vvv
```

### Issue: Permission denied

```bash
# Ensure correct SSH key permissions
chmod 600 ~/.ssh/devops-key.pem

# Verify user has sudo privileges
ansible all -m shell -a "sudo whoami"
```

### Issue: Docker not found

Run the setup playbook first:
```bash
ansible-playbook playbooks/setup.yml
```

## 📚 Additional Resources

- [Ansible Documentation](https://docs.ansible.com/)
- [Ansible Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html)
- [Ansible Galaxy](https://galaxy.ansible.com/) - Pre-built roles

## 🔄 CI/CD Integration

These playbooks can be integrated with GitLab CI/CD:

```yaml
deploy:production:
  stage: deploy
  script:
    - ansible-playbook ansible/playbooks/deploy.yml --limit production
  only:
    - main
  when: manual
```
