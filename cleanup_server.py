#!/usr/bin/env python3
"""
UpCloud Server Cleanup Script
This script helps you clean up (delete) servers created during testing.
"""

import os
import json
import time
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
                # Get server object and check its current state
                server = manager.get_server(server_info['uuid'])
                print(f"📊 Current server state: {server.state}")
                
                if server.state == 'started':
                    print("⏹️  Stopping server...")
                    server.stop()
                    
                    # Wait for the server to actually stop
                    print("⏳ Waiting for server to stop...")
                    max_wait = 60  # Maximum wait time in seconds
                    wait_time = 0
                    while wait_time < max_wait:
                        time.sleep(5)
                        wait_time += 5
                        
                        # Check server state
                        server = manager.get_server(server_info['uuid'])
                        print(f"   Server state: {server.state}")
                        
                        if server.state == 'stopped':
                            print("✅ Server has stopped!")
                            break
                        elif server.state == 'error':
                            print("❌ Server is in error state")
                            break
                    
                    if wait_time >= max_wait:
                        print("⏰ Timeout waiting for server to stop. Attempting deletion anyway...")
                        
                elif server.state == 'stopped':
                    print("✅ Server is already stopped!")
                    
                elif server.state == 'maintenance':
                    print("⚠️  Server is in maintenance mode, waiting...")
                    time.sleep(10)
                    
                else:
                    print(f"ℹ️  Server is in state: {server.state}")
                
                time.sleep(2)  # Small additional buffer
                
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
                            print(f"     📊 Current server state: {server.state}")
                            
                            if server.state == 'started':
                                print("     ⏹️  Stopping server...")
                                server.stop()
                                
                                # Wait for the server to actually stop
                                print("     ⏳ Waiting for server to stop...")
                                max_wait = 60  # Maximum wait time in seconds
                                wait_time = 0
                                while wait_time < max_wait:
                                    time.sleep(5)
                                    wait_time += 5
                                    
                                    # Check server state
                                    server = manager.get_server(server.uuid)
                                    print(f"        Server state: {server.state}")
                                    
                                    if server.state == 'stopped':
                                        print("     ✅ Server has stopped!")
                                        break
                                    elif server.state == 'error':
                                        print("     ❌ Server is in error state")
                                        break
                                
                                if wait_time >= max_wait:
                                    print("     ⏰ Timeout waiting for server to stop. Attempting deletion anyway...")
                                    
                            elif server.state == 'stopped':
                                print("     ✅ Server is already stopped!")
                                
                            elif server.state == 'maintenance':
                                print("     ⚠️  Server is in maintenance mode, waiting...")
                                time.sleep(10)
                                
                            else:
                                print(f"     ℹ️  Server is in state: {server.state}")
                            
                            time.sleep(2)  # Small additional buffer
                            
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
