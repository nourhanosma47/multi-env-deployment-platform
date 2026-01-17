# Terraform Infrastructure

This directory contains Terraform configurations to deploy the application infrastructure on AWS.

## 📋 Prerequisites

- Terraform 1.0+
- AWS CLI configured with credentials
- AWS account with appropriate permissions
- SSH key pair created in AWS

## 🏗️ Infrastructure Components

- **VPC**: Virtual Private Cloud with public subnets
- **Internet Gateway**: For public internet access
- **Security Groups**: For application and database isolation
- **EC2 Instance**: Application server (t2.micro)
- **Elastic IP**: Static public IP for the application

## 🚀 Usage

### 1. Initialize Terraform

```bash
terraform init
```

### 2. Create SSH Key Pair (if not exists)

```bash
# On AWS Console or using AWS CLI
aws ec2 create-key-pair --key-name devops-key --query 'KeyMaterial' --output text > devops-key.pem
chmod 400 devops-key.pem
```

### 3. Plan Infrastructure

```bash
terraform plan
```

### 4. Apply Infrastructure

```bash
terraform apply
```

Type `yes` when prompted.

### 5. Get Outputs

```bash
terraform output
```

This will show:
- Application server public IP
- SSH connection string
- Application URLs

## 📝 Configuration

### Customize Variables

Create a `terraform.tfvars` file:

```hcl
aws_region     = "us-east-1"
environment    = "production"
instance_type  = "t2.small"
project_name   = "my-devops-project"
```

### Multi-Environment Setup

Create environment-specific variable files:

```bash
# Development
terraform apply -var-file="environments/dev.tfvars"

# Staging
terraform apply -var-file="environments/staging.tfvars"

# Production
terraform apply -var-file="environments/prod.tfvars"
```

## 🔐 Security Notes

1. **Never commit** sensitive files:
   - `*.tfvars` (if contains secrets)
   - `*.pem` (SSH keys)
   - `terraform.tfstate` (contains sensitive data)

2. **Use AWS Secrets Manager** for production secrets

3. **Restrict SSH access** by updating security group CIDR blocks

## 📊 Cost Estimation

Approximate monthly costs (us-east-1):
- EC2 t2.micro: $8.50/month
- EBS Volume (20GB): $2.00/month
- Elastic IP: $3.60/month (if not attached)
- Data Transfer: Variable

**Total**: ~$10-15/month for basic setup

## 🧹 Cleanup

To destroy all resources:

```bash
terraform destroy
```

Type `yes` when prompted.

## 📚 Resources Created

| Resource | Type | Purpose |
|----------|------|---------|
| VPC | aws_vpc | Network isolation |
| Subnets | aws_subnet | Public subnets in multiple AZs |
| Internet Gateway | aws_internet_gateway | Internet access |
| Security Groups | aws_security_group | Firewall rules |
| EC2 Instance | aws_instance | Application server |
| Elastic IP | aws_eip | Static public IP |

## 🔧 Post-Deployment Steps

1. **SSH into instance**:
   ```bash
   ssh -i devops-key.pem ubuntu@<PUBLIC_IP>
   ```

2. **Clone repository**:
   ```bash
   cd /opt/app
   sudo git clone <your-repo-url> .
   ```

3. **Start application**:
   ```bash
   sudo docker-compose up -d
   ```

4. **Verify services**:
   ```bash
   sudo docker-compose ps
   ```

## 🐛 Troubleshooting

### Issue: Terraform can't find credentials

```bash
aws configure
# Enter your AWS Access Key ID and Secret Access Key
```

### Issue: Key pair doesn't exist

Create the key pair in AWS Console or CLI before running terraform apply.

### Issue: Instance not accessible

Check security group rules and ensure your IP is allowed for SSH.

## 📖 Additional Resources

- [Terraform AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)
