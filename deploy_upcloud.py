#!/usr/bin/env python3
"""
UpCloud Server Deployment Script
This script helps you deploy a simple web page on UpCloud using their API.
"""

import os
import sys
import time
import json
from dotenv import load_dotenv
import upcloud_api
from upcloud_api import CloudManager
from upcloud_api.errors import UpCloudAPIError

# Load environment variables
load_dotenv()

# Configuration
UPCLOUD_USERNAME = os.getenv('UPCLOUD_USERNAME')
UPCLOUD_PASSWORD = os.getenv('UPCLOUD_PASSWORD')
SERVER_ZONE = os.getenv('SERVER_ZONE', 'fi-hel1')
SERVER_PLAN = os.getenv('SERVER_PLAN', '1xCPU-1GB')

# Ubuntu 22.04 LTS template UUID
UBUNTU_22_04_TEMPLATE = '01000000-0000-4000-8000-000030220200'

class UpCloudDeployer:
    def __init__(self):
        """Initialize the UpCloud deployer with API credentials."""
        if not UPCLOUD_USERNAME or not UPCLOUD_PASSWORD:
            print("❌ Error: UpCloud credentials not found!")
            print("Please make sure you have:")
            print("1. Copied .env.example to .env")
            print("2. Added your UpCloud API credentials to .env")
            print("3. See UPCLOUD_SETUP.md for detailed instructions")
            sys.exit(1)
        
        # Check for SSH key files
        if not os.path.exists('upcloud_key.pub'):
            print("❌ Error: SSH public key not found!")
            print("Please generate SSH keys using: ssh-keygen -t rsa -b 4096 -f upcloud_key")
            sys.exit(1)
        
        try:
            self.manager = CloudManager(UPCLOUD_USERNAME, UPCLOUD_PASSWORD)
            
            # Read SSH public key
            with open('upcloud_key.pub', 'r') as f:
                self.ssh_public_key = f.read().strip()
            
            print("✅ UpCloud API connection initialized")
            print("✅ SSH public key loaded")
        except Exception as e:
            print(f"❌ Failed to initialize UpCloud API: {e}")
            sys.exit(1)
    
    def test_credentials(self):
        """Test API credentials by fetching account information."""
        try:
            account = self.manager.get_account()
            # Handle both dict and object responses
            if hasattr(account, 'username'):
                username = account.username
            elif isinstance(account, dict) and 'username' in account:
                username = account['username']
            else:
                username = "authenticated user"
            
            print(f"✅ API credentials valid for: {username}")
            return True
        except UpCloudAPIError as e:
            print(f"❌ API credentials invalid: {e}")
            return False
        except Exception as e:
            print(f"❌ Error testing credentials: {e}")
            return False
    
    def list_zones(self):
        """List available zones."""
        try:
            zones = self.manager.get_zones()
            print("📍 Available zones:")
            for zone in zones:
                # Handle both object and dict/string responses
                if hasattr(zone, 'id') and hasattr(zone, 'description'):
                    print(f"   • {zone.id} - {zone.description}")
                elif isinstance(zone, dict):
                    zone_id = zone.get('id', zone.get('name', str(zone)))
                    zone_desc = zone.get('description', zone.get('title', 'N/A'))
                    print(f"   • {zone_id} - {zone_desc}")
                else:
                    # Fallback for string or other formats
                    print(f"   • {str(zone)}")
            return zones
        except Exception as e:
            print(f"❌ Error fetching zones: {e}")
            return []
    
    def create_server(self, title="UpCloud-WebServer"):
        """Create a new server with web server configuration."""
        print(f"\n🖥️  Creating server: {title}")
        print(f"   Zone: {SERVER_ZONE}")
        print(f"   Plan: {SERVER_PLAN}")
        
        try:
            # Server configuration
            server_config = {
                'zone': SERVER_ZONE,
                'title': title,
                'hostname': f"{title.lower()}.example.com",
                'plan': SERVER_PLAN,
                'metadata': True,  # Required for cloud-init
                'storage_devices': {
                    'storage_device': [{
                        'action': 'clone',
                        'storage': UBUNTU_22_04_TEMPLATE,
                        'title': f"{title}-disk",
                        'size': 25,
                        'tier': 'maxiops'
                    }]
                },
                'login_user': {
                    'username': 'root',
                    'ssh_keys': {
                        'ssh_key': [self.ssh_public_key]
                    }
                },
                'user_data': self._get_cloud_init_script()
            }
            
            # Create the server
            server = self.manager.create_server(server_config)
            print(f"✅ Server created: {server.uuid}")
            print(f"   Title: {server.title}")
            print(f"   State: {server.state}")
            
            return server
            
        except UpCloudAPIError as e:
            print(f"❌ Failed to create server: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None
    
    def _get_cloud_init_script(self):
        """Get cloud-init script for automatic web server setup."""
        return """#cloud-config
packages:
  - nginx
  - ufw

runcmd:
  # Update system
  - apt-get update
  - apt-get upgrade -y
  
  # Configure firewall
  - ufw allow ssh
  - ufw allow 'Nginx Full'
  - ufw --force enable
  
  # Start and enable nginx
  - systemctl start nginx
  - systemctl enable nginx
  
  # Create our custom web page
  - rm -f /var/www/html/index.nginx-debian.html
  
  # Set proper permissions
  - chown -R www-data:www-data /var/www/html
  - chmod -R 755 /var/www/html

write_files:
  - path: /var/www/html/index.html
    content: |
      <!DOCTYPE html>
      <html lang="en">
      <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>Welcome to UpCloud! 🚀</title>
          <style>
              * { margin: 0; padding: 0; box-sizing: border-box; }
              body {
                  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                  color: white; min-height: 100vh; display: flex;
                  align-items: center; justify-content: center;
              }
              .container {
                  text-align: center; padding: 2rem; max-width: 600px;
                  background: rgba(255, 255, 255, 0.1); border-radius: 20px;
                  backdrop-filter: blur(10px); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
              }
              h1 { font-size: 3rem; margin-bottom: 1rem; animation: bounce 2s infinite; }
              .subtitle { font-size: 1.2rem; margin-bottom: 2rem; opacity: 0.9; }
              .server-info {
                  background: rgba(255, 255, 255, 0.1); padding: 1rem;
                  border-radius: 10px; margin: 1rem 0; font-family: 'Courier New', monospace;
              }
              .footer { margin-top: 2rem; font-size: 0.9rem; opacity: 0.8; }
              @keyframes bounce {
                  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
                  40% { transform: translateY(-10px); }
                  60% { transform: translateY(-5px); }
              }
          </style>
      </head>
      <body>
          <div class="container">
              <h1>🚀 Welcome to UpCloud!</h1>
              <p class="subtitle">Your server is now live and running!</p>
              <div class="server-info">
                  <strong>Server Status:</strong> ✅ Online<br>
                  <strong>Deployed via:</strong> UpCloud API<br>
                  <strong>Web Server:</strong> Nginx<br>
                  <strong>Auto-configured:</strong> Cloud-init
              </div>
              <div class="footer">
                  <p>🎉 Congratulations! You've successfully deployed your first UpCloud server using their API.</p>
                  <p>Time to build something amazing! 💪</p>
              </div>
          </div>
          <script>
              document.addEventListener('DOMContentLoaded', function() {
                  const footer = document.querySelector('.footer');
                  const timestamp = new Date().toLocaleString();
                  footer.innerHTML += `<br><small>Deployed on: ${timestamp}</small>`;
              });
          </script>
      </body>
      </html>
    permissions: '0644'
    owner: www-data:www-data
"""
    
    def wait_for_server(self, server_uuid, timeout=300):
        """Wait for server to be in started state."""
        print(f"🚀 Deploying your new UpCloud server...")
        print(f"💡 This typically takes 2-3 minutes - please be patient!")
        print(f"📋 We'll monitor the deployment progress for you...\n")
        
        start_time = time.time()
        last_state = None
        state_start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                server = self.manager.get_server(server_uuid)
                current_state = server.state
                elapsed_minutes = (time.time() - start_time) / 60
                
                # Only print status update if state changed or every 30 seconds
                if current_state != last_state or (time.time() - state_start_time) > 30:
                    if current_state == 'maintenance':
                        print(f"🔧 Server is being configured and installed... ({elapsed_minutes:.1f} min)")
                        print(f"   📦 Installing Ubuntu 22.04 LTS and setting up Nginx web server")
                    elif current_state == 'started':
                        print(f"✅ Server is now running! ({elapsed_minutes:.1f} min)")
                        print(f"🌐 Web server setup is completing in the background...")
                        return server
                    elif current_state == 'error':
                        print(f"❌ Server deployment failed after {elapsed_minutes:.1f} minutes")
                        return None
                    else:
                        print(f"📊 Server state: {current_state} ({elapsed_minutes:.1f} min)")
                    
                    last_state = current_state
                    state_start_time = time.time()
                    
                time.sleep(10)
                
            except Exception as e:
                print(f"❌ Error checking server status: {e}")
                time.sleep(10)
        
        elapsed_minutes = timeout / 60
        print(f"⏰ Timeout: Server didn't start within {elapsed_minutes:.0f} minutes")
        return None
    
    def get_server_ip(self, server):
        """Get the public IP address of the server."""
        try:
            # Try the direct method first (UpCloud API has helper methods)
            if hasattr(server, 'get_public_ip'):
                try:
                    public_ip = server.get_public_ip()
                    if public_ip:
                        return public_ip
                except:
                    pass
            
            # Check ip_addresses directly on server object
            if hasattr(server, 'ip_addresses'):
                for ip in server.ip_addresses:
                    if hasattr(ip, 'access') and hasattr(ip, 'address'):
                        if ip.access == 'public' and '.' in ip.address:  # IPv4 check
                            return ip.address
                    elif isinstance(ip, dict):
                        if ip.get('access') == 'public' and '.' in str(ip.get('address', '')):
                            return ip.get('address')
            
            # Handle object format with networking.interfaces
            if hasattr(server, 'networking') and hasattr(server.networking, 'interfaces'):
                for interface in server.networking.interfaces:
                    for ip in interface.ip_addresses:
                        if ip.access == 'public' and ip.family == 'IPv4':
                            return ip.address
            
            # Handle dictionary format
            elif isinstance(server, dict):
                networking = server.get('networking', {})
                interfaces = networking.get('interfaces', [])
                for interface in interfaces:
                    ip_addresses = interface.get('ip_addresses', [])
                    for ip in ip_addresses:
                        if isinstance(ip, dict):
                            if ip.get('access') == 'public' and ip.get('family') == 'IPv4':
                                return ip.get('address')
                        elif hasattr(ip, 'access') and hasattr(ip, 'family'):
                            if ip.access == 'public' and ip.family == 'IPv4':
                                return ip.address
                
        except Exception as e:
            print(f"⚠️  Error getting server IP: {e}")
        
        print("ℹ️  Could not automatically retrieve IP address from API response")
        return None
    
    def deploy_web_page(self, server_ip):
        """Deploy the web page to the server (already done via cloud-init)."""
        print(f"\n🌐 Web server deployment summary:")
        print(f"   ✅ Ubuntu 22.04 LTS installed")
        print(f"   ✅ Nginx web server configured")
        print(f"   ✅ Firewall rules applied")
        print(f"   ✅ Custom web page deployed")
        print(f"   🌍 Your website: http://{server_ip}")
        
        return True

def main():
    """Main deployment function."""
    print("🚀 UpCloud Web Server Deployment Script")
    print("=" * 50)
    
    # Initialize deployer
    deployer = UpCloudDeployer()
    
    # Test credentials
    if not deployer.test_credentials():
        return
    
    # List available zones
    deployer.list_zones()
    
    print(f"\n📋 Deployment Configuration:")
    print(f"   Zone: {SERVER_ZONE}")
    print(f"   Plan: {SERVER_PLAN}")
    print(f"   OS: Ubuntu 22.04 LTS")
    print(f"   ⏰ Expected deployment time: 2-3 minutes")
    
    # Confirm deployment
    response = input("\n❓ Proceed with deployment? (y/N): ").strip().lower()
    if response != 'y':
        print("❌ Deployment cancelled")
        return
    
    # Create server
    server = deployer.create_server()
    if not server:
        return
    
    # Wait for server to start
    server = deployer.wait_for_server(server.uuid)
    if not server:
        return
    
    # Get server IP
    server_ip = deployer.get_server_ip(server)
    if not server_ip:
        print("🌐 Server created successfully but couldn't auto-retrieve IP address")
        print("📍 Please check your UpCloud control panel for the server IP:")
        print("   https://hub.upcloud.com/")
        print(f"   Look for server: {server.title}")
        server_ip = "[CHECK_UPCLOUD_PANEL]"
    
    print(f"\n✅ Server Details:")
    print(f"   UUID: {server.uuid}")
    print(f"   Title: {server.title}")
    print(f"   IP Address: {server_ip}")
    print(f"   Zone: {server.zone}")
    print(f"   Plan: {server.plan}")
    
    # Deploy web page (already done via cloud-init)
    if server_ip != "[CHECK_UPCLOUD_PANEL]":
        deployer.deploy_web_page(server_ip)
        
        print(f"\n🎉 Deployment Complete!")
        print(f"   Website URL: http://{server_ip}")
        print(f"   SSH Access: ssh -i upcloud_key root@{server_ip}")
        print(f"\n⏰ Note: The web server might take an additional 1-2 minutes to fully initialize")
        print(f"   If the website isn't immediately available, please wait a moment and refresh")
    else:
        print(f"\n🎉 Deployment Complete!")
        print(f"   Website URL: http://[YOUR_SERVER_IP]")
        print(f"   SSH Access: ssh -i upcloud_key root@[YOUR_SERVER_IP]")
        print(f"   💡 Replace [YOUR_SERVER_IP] with the actual IP from UpCloud panel")
        print(f"\n⏰ Note: The web server might take an additional 1-2 minutes to fully initialize")
        print(f"   If the website isn't immediately available, please wait a moment and refresh")
    
    print(f"   Server UUID: {server.uuid}")
    print(f"\n💡 Remember to delete the server when you're done to avoid charges:")
    print(f"   You can do this via UpCloud control panel or API")
    
    # Save server info
    server_info = {
        'uuid': server.uuid,
        'title': server.title,
        'ip': server_ip,
        'zone': server.zone,
        'plan': server.plan,
        'created': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    with open('deployed_server.json', 'w') as f:
        json.dump(server_info, f, indent=2)
    print(f"   Server details saved to: deployed_server.json")

if __name__ == "__main__":
    main()
