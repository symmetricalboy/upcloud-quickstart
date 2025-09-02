# UpCloud Web Server Deployment 🚀

This project helps you deploy a simple web page on UpCloud using their API. Perfect for getting started with UpCloud and understanding how to automate server deployments!

**✨ Works on**: Windows (PowerShell), Linux, and macOS

## Quick Start

1. **Set up your UpCloud API credentials** (see [UPCLOUD_SETUP.md](UPCLOUD_SETUP.md) for detailed instructions)
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Configure environment**:
   - Bash/Linux: `cp .env.example .env`
   - PowerShell: `Copy-Item .env.example .env`
   - Then add your credentials to `.env`
4. **Deploy your server**: `python deploy_upcloud.py`
5. **Clean up when done**: `python cleanup_server.py`

## What This Does

- ✅ Creates a new UpCloud server via API
- 🔑 Uses SSH key authentication (secure, modern approach)
- 🐧 Deploys Ubuntu 22.04 LTS with automatic configuration
- 🌐 Sets up Nginx web server automatically
- 🎨 Deploys a beautiful example web page
- 🔒 Configures firewall for security
- 📊 Automatically retrieves and displays all connection details

## Files in This Project

- `deploy_upcloud.py` - Main deployment script
- `cleanup_server.py` - Server cleanup/deletion script
- `UPCLOUD_SETUP.md` - Detailed setup instructions
- `web_page/index.html` - Example web page (also embedded in deployment)
- `.env.example` - Environment variables template
- `requirements.txt` - Python dependencies
- `LICENSE` - MIT License

## Server Configuration

**Default Settings:**

- **Zone:** fi-hel1 (Finland, Helsinki)
- **Plan:** 1xCPU-1GB (perfect for testing)
- **OS:** Ubuntu 22.04 LTS
- **Storage:** 25GB SSD
- **Web Server:** Nginx (auto-configured)

You can change these in your `.env` file!

## Security Features

- 🔑 Uses dedicated API subaccount (recommended)
- 🔐 SSH key authentication (no passwords)
- 🛡️ Automatic firewall configuration
- 🔒 SSH and HTTP/HTTPS only
- 🚫 Prevents accidental credential commits (.gitignore)
- 🪟 Works on Windows PowerShell and Linux/macOS bash

## Cost Management

- 💰 Uses smallest available server plan
- 🕐 Easy cleanup script to delete test servers
- 📊 Server details saved for tracking
- ⚠️ Remember to delete servers when done!

## Need Help?

1. **Setup Issues?** Check [UPCLOUD_SETUP.md](UPCLOUD_SETUP.md)
2. **API Problems?** Verify your credentials in `.env`
3. **Server Not Starting?** Check UpCloud control panel
4. **Connection Issues?** Ensure firewall allows HTTP traffic
5. **IP Retrieval Issues?** The script will show UpCloud panel link if auto-retrieval fails

## Troubleshooting

**If deployment fails:**
- ✅ **SSH Key Missing?** Run: `ssh-keygen -t rsa -b 4096 -f upcloud_key`
- ✅ **API Credentials?** Double-check your `.env` file
- ✅ **IP Not Found?** Check UpCloud control panel at https://hub.upcloud.com/
- ✅ **Script Errors?** The script is resilient to UpCloud API format changes

## What's Next?

After your first deployment:

- 🌐 Access your website at the provided IP
- 🔗 Connect via SSH: `ssh -i upcloud_key root@{server_ip}`
- 🔗 Set up a domain name (optional)
- 📝 Replace the example web page with your own content
- 🔧 Explore UpCloud's advanced features
- 📈 Scale up when you're ready for production

## Support

- 📖 [UpCloud API Documentation](https://developers.upcloud.com/)
- 💬 [UpCloud Support](https://upcloud.com/support/)
- 🐛 Issues with this script? Check the code comments for troubleshooting

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Feel free to use, modify, and distribute this code as you see fit! 📄

---

Enjoy building with UpCloud! 🎉
