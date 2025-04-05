#/usr/bin/python3


import time
import requests
import subprocess
import os
from types import SimpleNamespace

# Here is an example of the JSON data returned from live-info:
#{"env":"production","schedulerTime":"2025-04-04 22:43:40","previous":{"starts":"2025-04-05 00:00:00.000000","ends":"2025-04-05 02:00:02.925714","type":"track","name":"Melo Grant - CulturalBunker040125","metadata":{"id":24070,"name":"","mime":"audio\/mp3","ftype":"audioclip","filepath":"imported\/16\/Melo Grant\/Cultural Bunker\/CulturalBunker040125.mp3","import_status":0,"currentlyaccessing":0,"editedby":null,"mtime":"2025-04-03 15:12:42","utime":"2025-04-03 15:12:05","lptime":"2025-04-05 00:00:02","md5":"311dc395e9d8e6b1889e6a3d2589cb97","track_title":"CulturalBunker040125","artist_name":"Melo Grant","bit_rate":320000,"sample_rate":44100,"format":null,"length":"02:00:02.925714","album_title":"Cultural Bunker","genre":"Show","comments":"","year":"2025","track_number":null,"channels":2,"url":null,"bpm":null,"rating":null,"encoded_by":null,"disc_number":null,"mood":null,"label":null,"composer":null,"encoder":null,"checksum":null,"lyrics":null,"orchestra":null,"conductor":null,"lyricist":null,"original_lyricist":null,"radio_station_name":null,"info_url":null,"artist_url":null,"audio_source_url":null,"radio_station_url":null,"buy_this_url":null,"isrc_number":null,"catalog_number":null,"original_artist":null,"copyright":null,"report_datetime":null,"report_location":null,"report_organization":null,"subject":null,"contributor":null,"language":null,"replay_gain":"-2.87","owner_id":16,"cuein":"00:00:00","cueout":"02:00:02.925714","hidden":false,"filesize":288118205,"description":"","artwork":"","track_type_id":null,"artwork_url":"https:\/\/airtime.993wbtv.org\/api\/track?id=24070&amp;return=artwork"}},"current":{"starts":"2025-04-05 02:00:00","ends":"2025-04-05 03:59:57.12645","type":"track","name":"DJ Llu - getFWDL_318_03302025","media_item_played":true,"metadata":{"id":24026,"name":"","mime":"audio\/mp3","ftype":"audioclip","filepath":"imported\/16\/getFWDL_318_03302025.mp3","import_status":0,"currentlyaccessing":0,"editedby":null,"mtime":"2025-03-31 17:23:26","utime":"2025-03-31 17:21:31","lptime":"2025-04-05 02:00:03","md5":"963036fdf6db97d189c725a4319b6d8f","track_title":"getFWDL_318_03302025","artist_name":"DJ Llu","bit_rate":160000,"sample_rate":44100,"format":null,"length":"01:59:57.12645","album_title":"Get Fresh With DJ Llu","genre":"Show","comments":"0","year":"2025","track_number":null,"channels":2,"url":null,"bpm":0,"rating":null,"encoded_by":null,"disc_number":null,"mood":"","label":"","composer":"","encoder":null,"checksum":null,"lyrics":null,"orchestra":null,"conductor":"","lyricist":null,"original_lyricist":null,"radio_station_name":null,"info_url":"","artist_url":null,"audio_source_url":null,"radio_station_url":null,"buy_this_url":null,"isrc_number":"","catalog_number":null,"original_artist":null,"copyright":"","report_datetime":null,"report_location":null,"report_organization":null,"subject":null,"contributor":null,"language":"","replay_gain":"-1.09","owner_id":16,"cuein":"00:00:00","cueout":"01:59:57.12645","hidden":false,"filesize":143944671,"description":"0","artwork":"","track_type_id":null,"artwork_url":"https:\/\/airtime.993wbtv.org\/api\/track?id=24026&amp;return=artwork"},"record":"0"},"next":{"starts":"2025-04-05 12:00:00.000000","ends":"2025-04-05 12:00:29.884082","type":"track","name":"Isabella Bufano - IsabellaBufano_GreenBubbleTea_StationIDPromo2.mp3","metadata":{"id":24056,"name":"","mime":"audio\/mp3","ftype":"audioclip","filepath":"imported\/16\/Isabella Bufano\/WBTV IDs\/IsabellaBufano_GreenBubbleTea_StationIDPromo2.mp3","import_status":0,"currentlyaccessing":0,"editedby":null,"mtime":"2025-04-01 15:34:31","utime":"2025-04-01 15:34:30","lptime":"2025-04-03 08:43:11","md5":"ddf96e970a10a62eb5d014e997987dd1","track_title":"IsabellaBufano_GreenBubbleTea_StationIDPromo2.mp3","artist_name":"Isabella Bufano","bit_rate":320000,"sample_rate":44100,"format":null,"length":"00:00:29.884082","album_title":"WBTV IDs","genre":"ID","comments":"","year":"2025","track_number":null,"channels":2,"url":null,"bpm":null,"rating":null,"encoded_by":null,"disc_number":null,"mood":null,"label":null,"composer":null,"encoder":null,"checksum":null,"lyrics":null,"orchestra":null,"conductor":null,"lyricist":null,"original_lyricist":null,"radio_station_name":null,"info_url":null,"artist_url":null,"audio_source_url":null,"radio_station_url":null,"buy_this_url":null,"isrc_number":null,"catalog_number":null,"original_artist":null,"copyright":null,"report_datetime":null,"report_location":null,"report_organization":null,"subject":null,"contributor":null,"language":null,"replay_gain":"-4.73","owner_id":16,"cuein":"00:00:00","cueout":"00:00:29.884082","hidden":false,"filesize":1200560,"description":"","artwork":"","track_type_id":null,"artwork_url":"https:\/\/airtime.993wbtv.org\/api\/track?id=24056&amp;return=artwork"}},"currentShow":[{"start_timestamp":"2025-04-04 22:00:00","end_timestamp":"2025-04-05 00:00:00","name":"Get Fresh With DJ Llu","description":"","id":6763,"instance_id":65462,"record":0,"url":"","image_path":"","starts":"2025-04-04 22:00:00","ends":"2025-04-05 00:00:00"}],"nextShow":[{"id":38416,"instance_id":68110,"name":"Bike Talk","description":"","url":"","start_timestamp":"2025-04-05 08:00:00","end_timestamp":"2025-04-05 09:00:00","starts":"2025-04-05 08:00:00","ends":"2025-04-05 09:00:00","record":0,"image_path":"","type":"show"}],"source_enabled":"Scheduled","timezone":"America\/New_York","timezoneOffset":"-14400","AIRTIME_API_VERSION":"1.1"}

# Here is an example of the config file
# api_url: "http://libretime-vm:8080/api"
# stream_url: "http://icecast2.993wbtv.org:8000/wbtv_fm_128"
# output_dir: "/path/to/recordings"
# output_file_format: "mp3"

# Change this to the path of your config file
config_path = "show_recorder.conf"

# stores all the config values
config = None

# a dictionary containing only the current show information, as fresh from the api
current_show = None

# an object with a snapshot of all the information about the 
# show being recorded, i.e., as it was from the api when the recording started
# it will be used after the recording is finished to provide the necessary tags and filename
# it is also used to check if the show is still being recorded
currently_recording_show = None

# an object with a snapshot of all the information about the
# show that needs to be finalized (i.e., the show that has just ended)
previously_recorded_show = None

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
    
def read_config():
    global config  # Declare config as global to modify it
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


def fetch_live_info():
    if not config or 'api_url' not in config.__dict__:
        raise ValueError("Configuration is missing or 'api_url' is not defined in the config file.")

    url = config.api_url + "/live-info"  # Use the API URL from the config file

    try:
        response = requests.get(url, timeout=10)  # Set a timeout for the request
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Parse and return the JSON response
    except requests.RequestException as e:
        print(f"Error fetching live info: {e}")
        return None

# start_recording_show is a function that will spawn a liquidsoap process to record the show
# it takes a current_show object as an argument
# it returns a currently_recording_show object that contains all the information about the show

def start_recording_show(current_show):      
    # Store the path of the temp recording in the returned object
    current_show['temp_path'] = temp_path = config.recording_temp_dir + "/" + current_show.get('name', 'N/A') + "." + config.output_file_format
    print(f"Starting recording for show: {current_show.get('name', 'N/A')}")

    # Create a Liquidsoap script to record the show
    # If the file exists already, it was probably interrupted and will just be appended to.
    with open("recording_script.liq", "w") as f:
        f.write(f"""
        set("log.level", 4)
        set("log.file", "liquidsoap.log")

        # Define the input stream
        input_stream = input.http("{config.stream_url}", id="input_stream")
        output_file = "{temp_path}"  # Temporary file to store the recording

        # Dump the stream into segmented files
        output.file(
        %mp3(bitrate = 96),
        fallible = true,
        flush = true,
        append = true,        
        {{"{current_show['temp_path']}"}},
        input_stream,
        reopen_when={{0m}}
        )

        """)
    # Run the Liquidsoap script to start recording
    try: 
        subprocess.run(["liquidsoap", "recording_script.liq"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting Liquidsoap: {e}")
        return None
    print(f"Recording started and saving to: {temp_path}")
    return current_show  # Return the currently recording show object

def finalize_recorded_show(previously_recorded_show):
    print(f"Finalizing recorded show: {previously_recorded_show.get('name', 'N/A')}")
    # Rename the file to include the show name and timestamp
    show_name = previously_recorded_show.get('name', 'N/A')
    start_time = previously_recorded_show.get('starts', 'N/A')
    end_time = previously_recorded_show.get('ends', 'N/A')
    output_format = getattr(config, 'output_file_format', 'mp3')  # Default to 'mp3' if not specified
    output_file = f"{config.output_dir}/{show_name}_{start_time}_{end_time}.{output_format}"
    # Move the file to the output directory
    subprocess.run(["mv", previously_recorded_show['temp_path'], output_file])
    print(f"Recorded show finalized and saved to: {output_file}")   


def main():
    global currently_recording_show
    global previously_recorded_show
    global recording_temp_dir

    read_config()
    
    print ("Config loaded successfully.")
    

    # Check if the config file is valid
    if not config or 'api_url' not in config.__dict__:
        print("Error: Configuration is missing or 'api_url' is not defined in the config file.")
        return

    # Create the show recorder temp dir if it doesn't exist
    recording_temp_dir = config.output_dir + "/recording_temp"
    if not os.path.exists(recording_temp_dir):
        os.makedirs(recording_temp_dir)
        print("Recording temp dir created at: ", recording_temp_dir)
    # Create the output dir if it doesn't exist
    if not os.path.exists(config.output_dir):
        os.makedirs(config.output_dir)
        print("Output dir created at: ", config.output_dir)
    
    
    live_info = LiveInfo()


    while True:

        ### Update the live info from the API
        print("Attempting to fetch live info...")
        data = fetch_live_info()
        if data:
            live_info.update(data)
            print("Live info updated successfully.")
            current_show = live_info.get_data().get('currentShow', [{}])[0]
            print("Current show:", current_show.get('name', 'N/A'))
            print("Start time:", current_show.get('starts', 'N/A'))
            print("End time:", current_show.get('ends', 'N/A'))            
        else:
            print("Failed to fetch live info. Retrying in next loop...")


        ### Check if the current show recording is in progress        
        if current_show:
            print(f"Current show: {current_show.get('name', 'N/A')}")

            # Uncomment this to skip show names that are on the config blocklist
            # if current_show.get('name') in config.blocklist_show_names:
            #     print(f"Skipping show {current_show.get('name', 'N/A')} as it is on the blocklist.")
            #     continue

            # Check the current time and compare it with the show start and end times
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            show_start = current_show.get('starts')
            show_end = current_show.get('ends')
            if show_start and show_end:
                if show_start <= current_time <= show_end:
                    print(f"Recording needs to be in progress for {current_show.get('name', 'N/A')}.")
                    # Check if the show is already being recorded
                    if (currently_recording_show is not None) and currently_recording_show.get('name') == current_show.get('name'):
                        print(f"Show {current_show.get('name', 'N/A')} is already being recorded.")
                        continue
                    else:
                        currently_recording_show = start_recording_show(current_show)
                else:
                    print(f"Show {current_show.get('name', 'N/A')} has ended.")
                    # Check if the show is still being recorded
                    if currently_recording_show and currently_recording_show.get('name') == current_show.get('name'):
                        print(f"Stopping recording for show: {currently_recording_show.get('name', 'N/A')}")
                        # Stop the recording process
                        subprocess.run(["pkill", "-f", "liquidsoap"])
                        # Move the currently_recording_show to the previous show
                        # and clear the currently_recording_show variable
                        previously_recorded_show = currently_recording_show
                        currently_recording_show = None
                        # Finalize the recorded show 
                        finalize_recorded_show(previously_recorded_show)
                    else:
                        print(f"No recording in progress for show: {current_show.get('name', 'N/A')}")
            else:
                print("Invalid start or end time for the current show.")
        else:
            print("No current show information available.")

        ### Check for any orphaned recordings in the temp directory
        # list files in the temp directory
        temp_files = os.listdir(config.recording_temp_dir)
        
        # If there are more than 1 files in the temp directory
        if len(temp_files) > 1:
            print("WARNING: Orphaned recordings found in temp directory")
            for file in temp_files:
                print (f"Found file: {file}")
                # If this is not the file that is currently being recorded
                # and not the file that was just finalized
                if (
                    (currently_recording_show and file != currently_recording_show.get('temp_path', None)) and
                    (previously_recorded_show and file != previously_recorded_show.get('temp_path', None))
                ):
                    # Delete the orphaned file
                    print(f"Deleting orphaned file: {file}")
                    # os.remove(file)
                
                
        

        
        
        time.sleep(15)  

if __name__ == "__main__":
    main()

