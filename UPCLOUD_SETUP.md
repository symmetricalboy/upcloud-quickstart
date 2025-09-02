# UpCloud Setup Guide 🚀

Welcome to your UpCloud deployment guide! This will help you get started with deploying a simple web page using the UpCloud API.

**Platform Support**: This guide includes commands for both **Linux/macOS (bash)** and **Windows (PowerShell)**.

## Step 1: Create Your UpCloud API Credentials

### Option A: Create a Dedicated API Subaccount (Recommended)

For security, it's best to create a dedicated API-only user:

1. **Log in to your UpCloud Control Panel**: https://hub.upcloud.com/
2. **Navigate to People**: Account → People
3. **Create subaccount**: Click "Create subaccount"
4. **Fill in the details**:
   - **Username**: Choose a unique username (e.g., `api-user-yourname`)
   - **Email**: Use your email (you can use `youremail+api@domain.com`)
   - **Password**: Create a strong password
   - **Permissions**:
     - ✅ **Allow API connections**
     - ❌ **Access to control panel** (uncheck this for security)

### Option B: Use Your Main Account (Less Secure)

If you prefer to use your main account credentials:

1. Go to Account → API
2. Note your main username and password

## Step 2: Set Up Your Environment

1. **Copy the environment file**:

   **Bash/Linux/macOS:**

   ```bash
   cp .env.example .env
   ```

   **PowerShell/Windows:**

   ```powershell
   Copy-Item .env.example .env
   ```

2. **Edit the .env file** with your actual credentials:

   ```env
   UPCLOUD_USERNAME=your_actual_api_username
   UPCLOUD_PASSWORD=your_actual_api_password
   ```

3. **Generate SSH keys for server access** (UpCloud now requires SSH key authentication):

   **Bash/Linux/macOS:**

   ```bash
   ssh-keygen -t rsa -b 4096 -f upcloud_key -N "" -C "upcloud-deployment"
   ```

   **PowerShell/Windows:**

   ```powershell
   ssh-keygen -t rsa -b 4096 -f upcloud_key -N "" -C "upcloud-deployment"
   ```

   This creates two files:
   - `upcloud_key` (private key - keep this secure!)
   - `upcloud_key.pub` (public key - this gets uploaded to your server)

## Step 3: Install Dependencies

**Bash/Linux/macOS:**

```bash
pip install -r requirements.txt
```

**PowerShell/Windows:**

```powershell
pip install -r requirements.txt
```

## Step 4: Run the Deployment Script

**Bash/Linux/macOS:**

```bash
python deploy_upcloud.py
```

**PowerShell/Windows:**

```powershell
python deploy_upcloud.py
```

This script will:

- ✅ Test your API credentials
- 🔑 Upload your SSH public key to the server
- 🖥️ Create a new server with SSH key authentication
- 🌐 Deploy a simple web page automatically via cloud-init
- 📄 Automatically retrieve and display the server IP address
- 📋 Provide you with the SSH connection command and all server details

## Available Zones

- `fi-hel1` - Finland, Helsinki (default)
- `fi-hel2` - Finland, Helsinki  
- `de-fra1` - Germany, Frankfurt
- `uk-lon1` - United Kingdom, London
- `us-chi1` - USA, Chicago
- `us-nyc1` - USA, New York
- `nl-ams1` - Netherlands, Amsterdam
- `sg-sin1` - Singapore

## Available Server Plans

- `1xCPU-1GB` - 1 vCPU, 1GB RAM (default)
- `1xCPU-2GB` - 1 vCPU, 2GB RAM
- `2xCPU-4GB` - 2 vCPU, 4GB RAM
- `4xCPU-8GB` - 4 vCPU, 8GB RAM

## Security Notes

- 🔒 Never commit your `.env` file to version control
- 🔑 Use a dedicated API subaccount for better security
- 🛡️ Consider setting up IP restrictions for your API user
- 🗑️ Delete test servers when you're done to avoid charges
- 🔐 Keep your SSH private key (`upcloud_key`) secure and never share it
- 📝 The SSH public key (`upcloud_key.pub`) is safe to share and gets uploaded to your server
- 🚫 Never commit SSH private keys to version control
- 🪟 **Windows users**: SSH keys work the same in PowerShell - no need for PuTTY or other tools

## Troubleshooting

**Common Issues & Solutions:**

- **"SSH public key not found"** → Run: `ssh-keygen -t rsa -b 4096 -f upcloud_key`
- **"CREATE_PASSWORD_INVALID"** → Fixed! Script now uses correct SSH key configuration
- **"METADATA_DISABLED_ON_CLOUD-INIT"** → Fixed! Script enables metadata automatically
- **IP address not retrieved** → Script shows UpCloud panel link as fallback
- **API format errors** → Fixed! Script handles multiple UpCloud API response formats

**If your server is created but script has errors:**
1. Check UpCloud control panel: https://hub.upcloud.com/
2. Look for your server and note the IP address
3. Connect with: `ssh -i upcloud_key root@[your-server-ip]`

## Need Help?

- 📖 [UpCloud API Documentation](https://developers.upcloud.com/)
- 💬 [UpCloud Support](https://upcloud.com/support/)
- 📧 Check your billing to monitor charges

## License

This project is open source and available under the MIT License. Feel free to use, modify, and share! 📄

---

Enjoy your UpCloud journey! 🎉
