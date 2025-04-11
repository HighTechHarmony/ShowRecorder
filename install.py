# Create a systemd service for the show recorder application
import subprocess
from types import SimpleNamespace
import os

# Change this to the path of your config file
# Currently it is set to the same directory as this script
# In the future, this should be a command line argument so that systemd can have some input on it
config_path = "show_recorder.conf"


def read_config():
    global config  
    # Config file is in format field=value
    config_dict = {}
    with open(config_path, "r") as f:
        for line in f:
            print(f"Reading line: {line.strip()}")
            if "=" in line:
                key, value = line.strip().split("=", 1)
                value = value.strip().strip('"').strip("'")
                config_dict[key.strip()] = value
    # Convert the dictionary to a SimpleNamespace for attribute-style access
    config = SimpleNamespace(**config_dict)
    

def create_showrecorder_service_file():
    print(f"Creating show_recorder service file for {config.runasuser} and {config.runasgroup}")
    service_content = f"""[Unit]
Description=Show Recorder Service
After=network.target
[Service]
Type=simple
ExecStart=/usr/bin/python3 {config.home_dir}/show_recorder.py
WorkingDirectory={config.home_dir}
User={config.runasuser}
Group={config.runasgroup}

StandardOutput=journal
StandardError=journal
Restart=always
RestartSec=5
[Install]
WantedBy=multi-user.target
"""
    # Write this out
    with open("show_recorder.service", "w") as f:
        f.write(service_content)
        

def create_api_service_file():
    print(f"Creating show_recorder_api service file for {config.runasuser} and {config.runasgroup}")
    service_content = f"""[Unit]
Description=Show Recorder API Service
After=network.target
[Service]
Type=simple 
ExecStart=/usr/bin/python3 {config.home_dir}/show_server_api.py
WorkingDirectory={config.home_dir}
User={config.runasuser}
Group={config.runasgroup}
StandardOutput=journal
StandardError=journal
Restart=always
RestartSec=5
[Install]
WantedBy=multi-user.target
"""
    # Write this out
    with open("show_recorder_api.service", "w") as f:
        f.write(service_content)

def main():
    read_config()
    create_showrecorder_service_file()
    create_api_service_file()
    # Check if the user is root
    if subprocess.run(["id", "-u"]).returncode != 0:
        print("This script must be run as root.")
        return

    service_file_path = "/etc/systemd/system"
    logrotate_file_path = "/etc/logrotate.d"

    print ("Do you want to install the logrotate configuration? (y/n)")
    answer = input().strip().lower()
    if answer == "y" or answer == "yes":
        print ("Enter your logrotate directory (default is /etc/logrotate.d):")
        logrotate_dir = input().strip()
        if not logrotate_dir:
            logrotate_dir = "/etc/logrotate.d"
        # Verify the directory exists
        if not os.path.exists(logrotate_dir):
            print(f"Logrotate directory '{logrotate_dir}' does not exist.")
            return
        # Create logrotate configuration
        logrotate_content = f"""{config.home_dir}/show_recorder.log {{
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 0640 {config.runasuser} {config.runasgroup}
    sharedscripts
    postrotate
        systemctl reload show_recorder.service > /dev/null 2>&1 || true
    endscript
}}
"""
        # Write this out
        with open(f"{logrotate_file_path}/show_recorder", "w") as f:
            f.write(logrotate_content)
        print(f"Logrotate configuration created at {logrotate_file_path}/show_recorder\n\n")
    else:
        print("Skipping logrotate configuration.")

    print ("Do you want to try to build and install the Web UI? (y/n)")
    answer = input().strip().lower()
    if answer == "y" or answer == "yes":
        # Build the web UI
        print("Building web UI...")
        
        subprocess.run(["npm", "install"], cwd="show-recorder-ui", check=True)
        subprocess.run(["npm", "run", "show-recorder-ut/build"], cwd="show-recorder-ui", check=True)
        print("Web UI built successfully.\n\n")
        print("Enter your web UI directory (default is /var/www/html):")
        web_ui_dir = input().strip()
        if not web_ui_dir:
            web_ui_dir = "/var/www/html"
        print(f"Copying web UI to {web_ui_dir}")
        subprocess.run(["sudo", "cp", "-r", "build", web_ui_dir], check=True)
        print(f"Web UI copied to {web_ui_dir}\n\n")
    else:
        print("Skipping web UI build.\n\n")



    
    print("Do you want to install and run the services? (y/n)")
    answer = input().strip().lower()
    if answer != "y" and answer != "yes":
        print("Exiting without installing services.")
        return

    # Copy the service file to the systemd directory
    print(f"Copying service file to {service_file_path}")
    subprocess.run(["sudo", "cp", "show_recorder.service", service_file_path], check=True)
    subprocess.run(["sudo", "cp", "show_recorder_api.service", service_file_path], check=True)
    subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True)
    subprocess.run(["sudo", "systemctl", "enable", "show_recorder.service"], check=True)
    subprocess.run(["sudo", "systemctl", "enable", "show_recorder_api.service"], check=True)
    subprocess.run(["sudo", "systemctl", "start", "show_recorder.service"], check=True)
    subprocess.run(["sudo", "systemctl", "start", "show_recorder_api.service"], check=True)

    print("Service files created and started successfully.")
    print("The API should be accessible at http://localhost:5000")
    # print("The web UI should be accessible at")
    print("Please check the status of the service with 'systemctl status show_recorder.service' and 'systemctl status show_recorder_api.service'.")
    print("Happy Recording!")

if __name__ == "__main__":
    main()
