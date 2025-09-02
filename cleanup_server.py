#!/usr/bin/env python3
"""
UpCloud Server Cleanup Script
This script helps you clean up (delete) servers created during testing.
"""

import os
import json
from dotenv import load_dotenv
from upcloud_api import CloudManager
from upcloud_api.errors import UpCloudAPIError

# Load environment variables
load_dotenv()

UPCLOUD_USERNAME = os.getenv('UPCLOUD_USERNAME')
UPCLOUD_PASSWORD = os.getenv('UPCLOUD_PASSWORD')

def main():
    """Main cleanup function."""
    print("🧹 UpCloud Server Cleanup Script")
    print("=" * 40)
    
    if not UPCLOUD_USERNAME or not UPCLOUD_PASSWORD:
        print("❌ Error: UpCloud credentials not found!")
        print("Please make sure your .env file is configured.")
        return
    
    try:
        manager = CloudManager(UPCLOUD_USERNAME, UPCLOUD_PASSWORD)
        print("✅ Connected to UpCloud API")
    except Exception as e:
        print(f"❌ Failed to connect to UpCloud API: {e}")
        return
    
    # Check for deployed server info
    if os.path.exists('deployed_server.json'):
        print("\n📄 Found deployed_server.json")
        with open('deployed_server.json', 'r') as f:
            server_info = json.load(f)
        
        print(f"   Server UUID: {server_info['uuid']}")
        print(f"   Title: {server_info['title']}")
        print(f"   IP: {server_info['ip']}")
        print(f"   Created: {server_info['created']}")
        
        response = input(f"\n❓ Delete server {server_info['title']} ({server_info['uuid']})? (y/N): ").strip().lower()
        if response == 'y':
            try:
                # Stop server first
                print("⏹️  Stopping server...")
                manager.stop_server(server_info['uuid'])
                
                # Delete server
                print("🗑️  Deleting server...")
                manager.delete_server(server_info['uuid'])
                
                print("✅ Server deleted successfully!")
                
                # Remove the server info file
                os.remove('deployed_server.json')
                print("✅ Cleaned up deployed_server.json")
                
            except UpCloudAPIError as e:
                print(f"❌ Failed to delete server: {e}")
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
        else:
            print("❌ Server deletion cancelled")
    
    # List all servers for manual cleanup
    print("\n🖥️  Listing all your servers:")
    try:
        servers = manager.get_servers()
        if not servers:
            print("   No servers found")
        else:
            for server in servers:
                print(f"   • {server.title} ({server.uuid}) - {server.state} - {server.zone}")
                
                # Offer to delete servers with 'UpCloud-WebServer' in the title
                if 'UpCloud-WebServer' in server.title:
                    response = input(f"     ❓ Delete this server? (y/N): ").strip().lower()
                    if response == 'y':
                        try:
                            if server.state == 'started':
                                print("     ⏹️  Stopping server...")
                                manager.stop_server(server.uuid)
                            
                            print("     🗑️  Deleting server...")
                            manager.delete_server(server.uuid)
                            print("     ✅ Server deleted!")
                            
                        except UpCloudAPIError as e:
                            print(f"     ❌ Failed to delete server: {e}")
                        except Exception as e:
                            print(f"     ❌ Unexpected error: {e}")
                            
    except Exception as e:
        print(f"❌ Error listing servers: {e}")
    
    print("\n🎉 Cleanup complete!")

if __name__ == "__main__":
    main()
