# Libretime ShowRecorder

## Uses the Libretime API to facilitate recording and storing shows

Have a hybrid (as in, live sometimes, automation sometimes) radio station, that runs Libretime? The LibreTime ShowRecorder is a great way to capture your shows to podcasts.

There are othe show recorders that work with Libretime, but this one allows you to separately specify the stream URL and the Libretime API URL. It also has some other interesting features:

- A block list so shows containing a keyword are not recorded
- Ability to specify an output directory, recording format, etc.
- A React web ui that allows you to browse, search, preview, and download recordings
- Recovery-minded operation, that is, if the internet connection is interrupted while a show recording is in progress, it should attempt to continue the current recording when able
- installer does most things required to get a system up and running (except nginx config)
- Very light weight

![Show Recorder Screen shot](https://smcgrath.com/hosted_images/showrecorder_screenshot.png "Show Recorder Screen shot")

## Dependencies

- Python3
- Nginx (react app)
- python3-flask (API and recording backend)
- liquidsoap (recording backend)
- Node JS (Web UI)

Tested with Node JS v18.19.0, Liquidsoap v2.1.3-2 on Debian Bookworm (12).

## Installation

Install liquidsoap. On Debian:
`sudo apt install liquidsoap`

Install python3-flask. On Debian:
`sudo apt install python3-flask`

Install nginx. On Debian:
`sudo apt install nginx`

Install node-js package manager. On Debian:
`sudo apt install npm`

Download the ShowRecorder:
`git clone https://github.com/HighTechHarmony/ShowRecorder`
`cd ShowRecorder`

You need a config file called show_recorder.conf in this directory. You can use provided `show_recorder.conf.example` as a starting point. Here is an example:

```
api_url = "https://my.libretime-server.com/api"
stream_url = "https://stream.server.com/source"
output_dir = "/mnt/Shows"
output_file_format = "mp3"
recording_temp_dir = "/tmp/recording_temp"
blocklist_show_names = ["ROTATION"]
log_level = "INFO"
home_dir = "/home/user/ShowRecorder"
runasuser= "user"
runasgroup= "user"
# delete_orphaned_files="true"
```

`api_url`: Set this to the URL your Libretime server with /api

`stream_url`: Set this to the URL of the stream to record from

`output_dir`: This is where completed recordings will be stored when they are complete. Could be local or mounted storage.

`output_file_format`: Choose your audio format, any of those supported by [Liquidsoap](https://www.liquidsoap.info)

`recording_temp_dir`: This is a temp directory where in-progress recordings are written. Should be local or very reliable.

`blocklist_show_names`: A list of keywords that, if contained in the show name, will be skipped

`log_level`: Can be "INFO", "DEBUG", "WARN", "ERROR"

`home_dir`: You can make this the location of the ShowRecorder directory you downloaded from git

`runasuser`/`runasgroup`: Change this to the system user you plan to run the ShowRecorder processes under. It is highly recommended that this be someone other than root.

`delete_orphaned_files`: This is an experimental option that will cause the show recorder to clear out old recordings in the temp folder that it doesn't recognize. Could reduce the recoverability of an interrupted recording, but could be helpful if you are worried about your system running out of temp space.

### Configure nginx

You need a basic web server and proxy for the API using nginx. Replacing /etc/nginx/sites-available/default with something like this should do well:

```
server {
    listen 80;
    server_name showrecorder.myserver.com;

    root /var/www/html;
    index index.html;

    location / {
        try_files $uri /index.html =404;
    }

    # Proxy configuration for API requests
    location /api {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Log files for debugging
    error_log /var/log/nginx/error.log;
    access_log /var/log/nginx/access.log;
}
```

Then restart nginx:
`sudo systemctl restart nginx`

### Build the UI and put it in place

```
cd ShowRecorder/show-recorder-ui
npm i
npm run build
sudo cp build/ /var/www/html -r
```

(Replace /var/www/html with whereever your public folder is)

### Run The Installer

`sudo python3 install.py`

It will ask you a few questions. If this is your first installation, you can probably just answer 'y' to them. about your logrotate.d location, create the system services, etc.

## Operation

When it's done, everything should be up and running. If there is a show on, you should be able to see it recording a file in the temp directory.

The web UI should be accessible at `http://showrecorder.myserver.com` or wherever your nginx server is.

The show recorder will log issues to `home_dir/show_recorder.log`.

## Other Recommendations

A cron job can be set up to prevent the recordings from filling up all available disk space.

```
crontab -e
```

And then add at the end something like:

```
# Delete recorded shows that are older than 90 days
0 2 * * * find /mnt/Shows -type f -mtime +90 -exec rm -f {} \;
```

Remember that the user you set it up on needs to have write access to the show storage location.
