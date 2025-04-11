#/usr/bin/python3


import time
import logging
from datetime import datetime
import requests
import subprocess
import os
import signal  # Add signal module for handling termination signals
import html
from types import SimpleNamespace

# Here is an example of the JSON data returned from live-info:
#{"env":"production","schedulerTime":"2025-04-04 22:43:40","previous":{"starts":"2025-04-05 00:00:00.000000","ends":"2025-04-05 02:00:02.925714","type":"track","name":"Melo Grant - CulturalBunker040125","metadata":{"id":24070,"name":"","mime":"audio\/mp3","ftype":"audioclip","filepath":"imported\/16\/Melo Grant\/Cultural Bunker\/CulturalBunker040125.mp3","import_status":0,"currentlyaccessing":0,"editedby":null,"mtime":"2025-04-03 15:12:42","utime":"2025-04-03 15:12:05","lptime":"2025-04-05 00:00:02","md5":"311dc395e9d8e6b1889e6a3d2589cb97","track_title":"CulturalBunker040125","artist_name":"Melo Grant","bit_rate":320000,"sample_rate":44100,"format":null,"length":"02:00:02.925714","album_title":"Cultural Bunker","genre":"Show","comments":"","year":"2025","track_number":null,"channels":2,"url":null,"bpm":null,"rating":null,"encoded_by":null,"disc_number":null,"mood":null,"label":null,"composer":null,"encoder":null,"checksum":null,"lyrics":null,"orchestra":null,"conductor":null,"lyricist":null,"original_lyricist":null,"radio_station_name":null,"info_url":null,"artist_url":null,"audio_source_url":null,"radio_station_url":null,"buy_this_url":null,"isrc_number":null,"catalog_number":null,"original_artist":null,"copyright":null,"report_datetime":null,"report_location":null,"report_organization":null,"subject":null,"contributor":null,"language":null,"replay_gain":"-2.87","owner_id":16,"cuein":"00:00:00","cueout":"02:00:02.925714","hidden":false,"filesize":288118205,"description":"","artwork":"","track_type_id":null,"artwork_url":"https:\/\/airtime.993wbtv.org\/api\/track?id=24070&amp;return=artwork"}},"current":{"starts":"2025-04-05 02:00:00","ends":"2025-04-05 03:59:57.12645","type":"track","name":"DJ Llu - getFWDL_318_03302025","media_item_played":true,"metadata":{"id":24026,"name":"","mime":"audio\/mp3","ftype":"audioclip","filepath":"imported\/16\/getFWDL_318_03302025.mp3","import_status":0,"currentlyaccessing":0,"editedby":null,"mtime":"2025-03-31 17:23:26","utime":"2025-03-31 17:21:31","lptime":"2025-04-05 02:00:03","md5":"963036fdf6db97d189c725a4319b6d8f","track_title":"getFWDL_318_03302025","artist_name":"DJ Llu","bit_rate":160000,"sample_rate":44100,"format":null,"length":"01:59:57.12645","album_title":"Get Fresh With DJ Llu","genre":"Show","comments":"0","year":"2025","track_number":null,"channels":2,"url":null,"bpm":0,"rating":null,"encoded_by":null,"disc_number":null,"mood":"","label":"","composer":"","encoder":null,"checksum":null,"lyrics":null,"orchestra":null,"conductor":"","lyricist":null,"original_lyricist":null,"radio_station_name":null,"info_url":"","artist_url":null,"audio_source_url":null,"radio_station_url":null,"buy_this_url":null,"isrc_number":"","catalog_number":null,"original_artist":null,"copyright":"","report_datetime":null,"report_location":null,"report_organization":null,"subject":null,"contributor":null,"language":"","replay_gain":"-1.09","owner_id":16,"cuein":"00:00:00","cueout":"01:59:57.12645","hidden":false,"filesize":143944671,"description":"0","artwork":"","track_type_id":null,"artwork_url":"https:\/\/airtime.993wbtv.org\/api\/track?id=24026&amp;return=artwork"},"record":"0"},"next":{"starts":"2025-04-05 12:00:00.000000","ends":"2025-04-05 12:00:29.884082","type":"track","name":"Isabella Bufano - IsabellaBufano_GreenBubbleTea_StationIDPromo2.mp3","metadata":{"id":24056,"name":"","mime":"audio\/mp3","ftype":"audioclip","filepath":"imported\/16\/Isabella Bufano\/WBTV IDs\/IsabellaBufano_GreenBubbleTea_StationIDPromo2.mp3","import_status":0,"currentlyaccessing":0,"editedby":null,"mtime":"2025-04-01 15:34:31","utime":"2025-04-01 15:34:30","lptime":"2025-04-03 08:43:11","md5":"ddf96e970a10a62eb5d014e997987dd1","track_title":"IsabellaBufano_GreenBubbleTea_StationIDPromo2.mp3","artist_name":"Isabella Bufano","bit_rate":320000,"sample_rate":44100,"format":null,"length":"00:00:29.884082","album_title":"WBTV IDs","genre":"ID","comments":"","year":"2025","track_number":null,"channels":2,"url":null,"bpm":null,"rating":null,"encoded_by":null,"disc_number":null,"mood":null,"label":null,"composer":null,"encoder":null,"checksum":null,"lyrics":null,"orchestra":null,"conductor":null,"lyricist":null,"original_lyricist":null,"radio_station_name":null,"info_url":null,"artist_url":null,"audio_source_url":null,"radio_station_url":null,"buy_this_url":null,"isrc_number":null,"catalog_number":null,"original_artist":null,"copyright":null,"report_datetime":null,"report_location":null,"report_organization":null,"subject":null,"contributor":null,"language":null,"replay_gain":"-4.73","owner_id":16,"cuein":"00:00:00","cueout":"00:00:29.884082","hidden":false,"filesize":1200560,"description":"","artwork":"","track_type_id":null,"artwork_url":"https:\/\/airtime.993wbtv.org\/api\/track?id=24056&amp;return=artwork"}},"currentShow":[{"start_timestamp":"2025-04-04 22:00:00","end_timestamp":"2025-04-05 00:00:00","name":"Get Fresh With DJ Llu","description":"","id":6763,"instance_id":65462,"record":0,"url":"","image_path":"","starts":"2025-04-04 22:00:00","ends":"2025-04-05 00:00:00"}],"nextShow":[{"id":38416,"instance_id":68110,"name":"Bike Talk","description":"","url":"","start_timestamp":"2025-04-05 08:00:00","end_timestamp":"2025-04-05 09:00:00","starts":"2025-04-05 08:00:00","ends":"2025-04-05 09:00:00","record":0,"image_path":"","type":"show"}],"source_enabled":"Scheduled","timezone":"America\/New_York","timezoneOffset":"-14400","AIRTIME_API_VERSION":"1.1"}

# Change this to the path of your config file
# Currently it is set to the same directory as this script
# In the future, this should be a command line argument so that systemd can have some input on it
config_path = "show_recorder.conf"

# This is where the logs will be stored. Again, this should be a command line argument
log_path = "show_recorder.log"

# stores all the config values
config = None

# an object with a snapshot of all the information about the 
# show being recorded, i.e., as it was from the api when the recording started
# it will be used after the recording is finished to provide the necessary tags and filename
# it is also used to check if the show is still being recorded
# it will be outfitted with a pid to track the liquidsoap process
# If this is None, it means that there is no show currently being recorded
currently_recording_show = None

# This is primarly used so that we can finalize the previously recorded show file
# Without it being treated like an orphan
previously_recorded_show = None

# A global for tracking the pid of liquidsoap, in case of a kill signal
liquidsoap_pid = None



# This class is used to store the big chunk of all live info data
# This includes info about the previous, current, and next shows
# Source enabled, timezone, API version, and a bunch of other stuff
class LiveInfo:
    def __init__(self):
        self.data = None

    def update(self, new_data):
        self.data = new_data

    def get_data(self):
        return self.data


def setup_logging():
    # Get log file and log level from config
    log_file = getattr(config, 'logfile', log_path)  # Default to 'show_recorder.log'
    log_level = getattr(config, 'log_level', 'info').upper()  # Default to 'info'

    # Map log level strings to logging module levels
    log_levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARN': logging.WARNING,
        'ERROR': logging.ERROR
    }
    level = log_levels.get(log_level, logging.INFO)  # Default to INFO if invalid level

    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(level)

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_formatter = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    logging.info("Logging initialized.")


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
    setup_logging()  # Set up logging after reading the config


# Fetches the live info from the API and returns it as a JSON object
def fetch_live_info():
    if not config or 'api_url' not in config.__dict__:
        raise ValueError("Configuration is missing or 'api_url' is not defined in the config file.")

    url = config.api_url + "/live-info"  # Use the API URL from the config file

    try:
        response = requests.get(url, timeout=10)  # Set a timeout for the request
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Parse and return the JSON response
    except requests.RequestException as e:
        logging.error("Error fetching live info: %s",{e})
        return None


# start_recording is a function that will spawn a process to record the show
# It stores important information in the global show object such as the file name and temp path
# It generates a Liquidsoap script to record the show and spawns a Liquidsoap process to run it

def start_recording():      
    global currently_recording_show
    global previously_recorded_show
    global liquidsoap_pid

    logging.debug("start_recording()")

    show_name = currently_recording_show.get('name', 'N/A')
    start_time = currently_recording_show.get('starts', 'N/A').replace(" ", "_").replace(":", "-")
    end_time = currently_recording_show.get('ends', 'N/A').replace(" ", "_").replace(":", "-")    
    output_format = getattr(config, 'output_file_format', 'mp3')  # Default to 'mp3' if not specified
    output_bitrate = getattr(config, 'output_bitrate', 96) # Default to 96 kbps if not specified

    # Generate the file name and store it in the currently_recording_show object
    file_name =  f"{show_name}_- [{start_time}]_- [{end_time}].{output_format}"
    # Replace any really bad characters from the file name
    file_name = file_name.replace(":", "-").replace("/", "-").replace("\\", "-").replace(" ", "_")
    # Unescape HTML entities with their unicode equivalents
    file_name = html.unescape(file_name)

    # Remove any leading or trailing spaces
    file_name = file_name.strip()    

    currently_recording_show['file_name'] = file_name 
    currently_recording_show['temp_path'] = temp_path = config.recording_temp_dir 

    logging.debug("Creating Liquidsoap script to record the show.")
    # Create a Liquidsoap script to record the show
    # If the output.file exists already, it was probably interrupted and will just be appended to.
    
    with open("recording_script.liq", "w") as f:
        f.write(f"""
set("log.level", 4)
set("log.file", "liquidsoap.log")

input_stream = input.http("{config.stream_url}", id="input_stream")

output_file = "{temp_path}/{file_name}"
output.file(
    %mp3(bitrate = {output_bitrate}),
    fallible = true,
    flush = true,
    append = true,        
    output_file,
    input_stream,
    reopen_when={{0m}}
)

        """)
    # Run the Liquidsoap script to start recording
    try: 
        logging.info("Starting recording for show: %s", currently_recording_show.get('name', 'N/A'))        
        process = subprocess.Popen(["liquidsoap", "recording_script.liq"])
        logging.debug("Liquidsoap process started with PID: %s",process.pid)
        # Store the PID in the currently_recording_show object
        currently_recording_show['pid'] = process.pid
        # Also store it in the global variable for signal handling
        liquidsoap_pid = process.pid
    except subprocess.SubprocessError as e:
        print(f"Error starting Liquidsoap: {e}")
        return None
    logging.debug("Recording started and saving to: %s",temp_path)
    

def stop_recording():
    # Get pid from show    
    pid = currently_recording_show.get('pid', None)
    print(f"Stopping recording for PID: {pid}")
    
    # Terminate the Liquidsoap process
    try:
        subprocess.run(["kill", str(pid)], check=True)
        print(f"Liquidsoap process with PID {pid} terminated.")
    except subprocess.CalledProcessError as e:
        print(f"Error stopping Liquidsoap process: {e}")

# This will stop any currently recording show, and will start a new one if it's not on the blocklist
def try_to_change_to(new_show):
    global currently_recording_show
    global previously_recorded_show

    logging.debug("try_to_change_to(%s)", new_show.get('name', 'N/A'))

    # Anyway you look at it, this is a new show, so if there is currently a show recording, stop it
    if currently_recording_show is not None:
        logging.info("Stopping recording for show: %s", currently_recording_show.get('name', 'N/A'))
        stop_recording()    
    
    # unless the new show is on the blocklist, do the shuffle and call start recording
    if new_show.get('name') in getattr(config, 'blocklist_show_names', []):
        logging.debug("Not doing anything with this show %s, as it is on the blocklist.", new_show.get('name', 'N/A'))        
    else:
        # Shuffle
        previously_recorded_show = currently_recording_show
        currently_recording_show = new_show

        # Start recording the new show
        start_recording()
        
        logging.info(f"Recording started for show: {currently_recording_show.get('name', 'N/A')}")
    
    # If there is a newly previously recorded show, finalize it
    if previously_recorded_show:
        logging.info("Finalizing previously recorded show: %s", previously_recorded_show.get('name', 'N/A'))
        # Finalize the previously recorded show
        finalize_recorded(previously_recorded_show)
        previously_recorded_show = None
        
    
# This essentially takes a show object and moves it to the configured output directory
def finalize_recorded(show):
    logging.info("Finalizing recorded show: %s",show.get('name', 'N/A'))
    # Rename the file to include the show name and timestamp
    show_name = show.get('name', 'N/A')
    start_time = show.get('starts', 'N/A')
    end_time = show.get('ends', 'N/A')
    output_format = getattr(config, 'output_file_format', 'mp3')  # Default to 'mp3' if not specified
    # output_file = f"{config.output_dir}/{show_name}_{start_time}_{end_time}.{output_format}"
    # Here we would inject tags, etc. if that is something we want to do in the future
    
    # Move the file from wherever it is to the configured output directory
    temp_path = show.get('temp_path', 'N/A')
    file_name = show.get('file_name', 'N/A')
    subprocess.run(["mv", f"{temp_path}/{file_name}", f"{config.output_dir}/{file_name}"], check=True)
    logging.info("Recording finalized and moved to: %s",config.output_dir + "/" + file_name)


def signal_handler(signum, frame):
    global liquidsoap_pid
    print(f"Received signal {signum}. Terminating gracefully...")
    if liquidsoap_pid:
        print(f"Stopping Liquidsoap process with PID: {liquidsoap_pid}")
        try:
            subprocess.run(["kill", str(liquidsoap_pid)], check=True)
            print(f"Liquidsoap process with PID {liquidsoap_pid} terminated.")
        except subprocess.CalledProcessError as e:
            print(f"Error stopping Liquidsoap process: {e}")
    print("Exiting...")
    exit(0)

# Register signal handlers
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)


def main():
    global currently_recording_show
    global previously_recorded_show
    global config    

    read_config()
    
    logging.info("Config loaded successfully.")
    

    # Check if the config file is valid
    if not config or 'api_url' not in config.__dict__:
        print("Error: Configuration is missing or 'api_url' is not defined in the config file.")
        return

    # Create the show recorder temp dir if it doesn't exist    
    if not os.path.exists(config.recording_temp_dir):
        os.makedirs(config.recording_temp_dir)
        print("Recording temp dir created at: ", config.recording_temp_dir)
    # Create the output dir if it doesn't exist
    if not os.path.exists(config.output_dir):
        os.makedirs(config.output_dir)
        print("Output dir created at: ", config.output_dir)
    
    
    live_info = LiveInfo()

    # Every minute, we see what maintenance tasks we need to do
    while True:
        logging.info("Starting loop.")

        ### Retry loop for fetching live info and processing currentShow
        retry_count = 0
        max_retries = 58 # When something goes wrong, retry for 58 seconds (1 minute) to get valid data
        while retry_count < max_retries:
            logging.debug("Attempting to fetch live info (Retry %d/%d)...", retry_count + 1, max_retries)
            data = fetch_live_info()
            if data:
                live_info.update(data)
                logging.debug("Live info updated successfully.")

                # Check for valid currentShow
                current_show_list = live_info.get_data().get('currentShow', [])
                if current_show_list:
                    current_show_api = current_show_list[0]
                    logging.debug("Current show: %s", current_show_api.get('name', 'N/A'))
                    logging.debug("Start time: %s", current_show_api.get('starts', 'N/A'))
                    logging.debug("End time: %s", current_show_api.get('ends', 'N/A'))
                    break  # Exit the retry loop once valid data is fetched and processed
                else:
                    logging.warning("currentShow is invalid or missing. Retrying in 1 second...")
            else:
                logging.warning("Failed to fetch live info. Retrying in 1 second...")

            retry_count += 1
            time.sleep(1)  # Wait for 1 second before retrying

        if retry_count >= max_retries:
            logging.error("Max retries reached (%d). Continuing to the main loop...", max_retries)

        # Compare the current show with the currently recording show
        # If they are different, or if there is no currently recording show, we need to handle the show change
        if currently_recording_show is None or current_show_api.get('name') != currently_recording_show.get('name'):
            logging.debug("Show change detected.")
            try_to_change_to(current_show_api)
        else:
            logging.debug("No show change detected.")

        ### Check for any orphaned recordings in the temp directory        
        temp_files = os.listdir(config.recording_temp_dir)
        
        # There should never be more than 2 files in the temp directory 
        # (the one being recorded and the one that is being finalized)
        if len(temp_files) > 1:
            logging.warning("WARNING: Possibly orphaned recordings found in temp directory")
            for file in temp_files:
                logging.debug ("    Found file: %s",file)
                # If this is not the file that is currently being recorded
                # and not the file that was just finalized
                if (currently_recording_show is not None and file == currently_recording_show.get('file_name', None)):
                    logging.debug("    It's okay, %s is currently being recorded",file)
                else:
                    if (previously_recorded_show is not None and file == previously_recorded_show.get('file_name', None)):
                        logging.debug("    It's okay, %s is currently being finalized",file)                        
                    else:
                        try:
                            if getattr(config, "delete_orphaned_files", "false").lower() == "true":
                                logging.info("config.delete_orphaned_files is true, deleting file: %s", file)
                                os.remove(config.recording_temp_dir + "/" + file)
                            else:
                                logging.debug("Not configured to delete orphaned files, will keep file: %s", file)
                        except Exception as e:
                            logging.error("Error while handling orphaned file '%s': %s", file, str(e))

        
        # Calculate the time until the next minute
        now = datetime.now()
        seconds_until_next_minute = 60 - now.second
        time.sleep(seconds_until_next_minute)

if __name__ == "__main__":
    main()

