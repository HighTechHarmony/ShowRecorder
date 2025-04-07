# Create a systemd service for the show recorder application
import subprocess
from types import SimpleNamespace

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
    

def create_service_file():
    print(f"Creating service file for {config.runasuser} and {config.runasgroup}")
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
        



def main():
    read_config()
    create_service_file()

    service_file_path = "/etc/systemd/system/"

    # Copy the service file to the systemd directory
    print(f"Copying service file to {service_file_path}")
    subprocess.run(["sudo", "cp", "show_recorder.service", service_file_path], check=True)
    subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True)
    subprocess.run(["sudo", "systemctl", "enable", "show_recorder.service"], check=True)
    subprocess.run(["sudo", "systemctl", "start", "show_recorder.service"], check=True)

if __name__ == "__main__":
    main()
