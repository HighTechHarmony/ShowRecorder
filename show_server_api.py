import os
import re
import html
from flask import Flask, jsonify, send_from_directory, abort, request
from types import SimpleNamespace

# Read configuration
config_path = "show_recorder.conf"
config = None

def read_config():
    global config
    config_dict = {}
    with open(config_path, "r") as f:
        for line in f:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                value = value.strip().strip('"').strip("'")
                config_dict[key.strip()] = value
    config = SimpleNamespace(**config_dict)

# Initialize Flask app
app = Flask(__name__)

# Read the configuration
read_config()

# Ensure the output directory exists
if not os.path.exists(config.output_dir):
    raise FileNotFoundError(f"Output directory '{config.output_dir}' does not exist.")

# Compile the blocklist regex pattern
blocklist_pattern = getattr(config, "blocklist_show_names", None)
# Strip non-alphanumeric characters from the blocklist pattern
if blocklist_pattern:
    blocklist_pattern = re.sub(r"[^a-zA-Z0-9\s]", "", blocklist_pattern)
    # Replace spaces with _
    blocklist_pattern = blocklist_pattern.replace(" ", "_")
    print (f"Blocklist pattern: {blocklist_pattern}")
blocklist_regex = re.compile(blocklist_pattern) if blocklist_pattern else None

# Allowed audio file extensions
ALLOWED_EXTENSIONS = {".mp3", ".wav", ".flac", ".aac", ".ogg"}

def is_audio_file(filename):
    """Check if a file is an audio file based on its extension."""
    return any(filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS)

def is_blocked(filename):
    """Check if a file matches the blocklist regex."""
    # return blocklist_regex and blocklist_regex.search(filename)
    return False  # Temporarily disable blocklist check, for testing purposes

def rewrite_filename(filename):
    """
    Rewrites a filename by replacing HTML entities with their correct characters.
    """
    return html.unescape(filename)

# This is just a dead simple list of the files in the output directory
@app.route("/api/list_files", methods=["GET"])
def list_files():
    """List all audio files in the output directory, excluding blocklisted files."""
    try:
        # Get the optional 'filter' query parameter
        search_filter = request.args.get("filter", "").lower()

        files = []
        for file in os.listdir(config.output_dir):
            if is_audio_file(file) and not is_blocked(file):
                # Apply the search filter if provided
                if search_filter in file.lower():
                    files.append(file)

        return jsonify({"files": files})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# This is the main endpoint for the show server, it is fully featured 
# besides the filename, it parses and gives the show name, start time, end time, and chunk number
@app.route("/api/list_shows", methods=["GET"])
def list_shows():
    """List all shows files in the output directory, excluding blocklisted files.
    This provides useful parsed information into the response, derived from the filename 
    """
    try:
        # Get the optional 'filter' query parameter
        search_filter = request.args.get("filter", "").lower()

        files = []
        for file in os.listdir(config.output_dir):
            if is_audio_file(file) and not is_blocked(file):
                # Apply the search filter if provided
                if search_filter in file.lower():
                    file_path = os.path.join(config.output_dir, file)
                    file_size = os.path.getsize(file_path)  # Get the file size in bytes
                    files.append([file, file_size])  # Append a two-element array with filename and size

        # Parse the show names from the filenames
        shows = []
        for file,file_size in files:
            # Rewrite the filename to handle HTML entities
            file = rewrite_filename(file)

            # File format is: show_name_-_[start_time]_[end_time]_-_[chunk_number].mp3
            # If there is no chunk number, it is not a chunked file, chunk_number will be 1

            # show name is everything to the left of the first '_-_['
            show_name = file.split("_-_")[0]
            # replace _ with spaces
            show_name = show_name.replace("_", " ")

            # start_date_start_time is everything between the first [ and the first ]
            start_datetime = file.split("[")[1].split("]")[0]
            # start date is everything to the left of the first space
            start_date = start_datetime.split("_")[0]
            
            # start time is everything to the right of the first space
            start_time = start_datetime.split("_")[1]
            #replace hyphens with colons
            start_time = start_time.replace("-", ":")

            # end date_end_time is everything between the second [ and the second ]
            end_datetime = file.split("[")[2].split("]")[0]
            # end date is everything to the left of the first space
            end_date = end_datetime.split("_")[0]
            # end time is everything to the right of the first space
            end_time = end_datetime.split("_")[1]
            # chunk number is a number to the right of the last ']' and left of the last '.' before the extension
            chunk_number = file.split("]")[-1].split(".")[0]
            # If there is no chunk number, it is not a chunked file, chunk_number will be 1
            if chunk_number == "":
                chunk_number = 1
            else:
                chunk_number = int(chunk_number)


            show = {
                "filename": file,
                "name": show_name,
                "start_time": start_time,
                "start_date": start_date,
                "end_time": end_time,
                "end_date": end_date,
                "size": file_size,
                "chunk_number": chunk_number
            }
            # Add the show to the list
            shows.append(show)

        # Return as json
        return jsonify({"shows": shows})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/files/<filename>", methods=["GET"])
def download_file(filename):
    """Serve an audio file for download."""
    try:
        if not is_audio_file(filename):
            abort(400, description="Invalid file type.")
        if is_blocked(filename):
            abort(403, description="File is blocklisted.")
        return send_from_directory(config.output_dir, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404, description="File not found.")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Run the Flask app
    app.run(host="::", port=5000, debug=True)