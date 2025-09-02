# UpCloud Setup Guide 🚀

Welcome to your UpCloud deployment guide! This will help you get started with deploying a simple web page using the UpCloud API.

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

   ```bash
   cp .env.example .env
   ```

2. **Edit the .env file** with your actual credentials:

   ```env
   UPCLOUD_USERNAME=your_actual_api_username
   UPCLOUD_PASSWORD=your_actual_api_password
   ```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Run the Deployment Script

```bash
python deploy_upcloud.py
```

This script will:

- ✅ Test your API credentials
- 🖥️ Create a new server
- 🌐 Deploy a simple web page
- 📄 Provide you with the server IP address

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

## Need Help?

- 📖 [UpCloud API Documentation](https://developers.upcloud.com/)
- 💬 [UpCloud Support](https://upcloud.com/support/)
- 📧 Check your billing to monitor charges

Enjoy your UpCloud journey! 🎉
