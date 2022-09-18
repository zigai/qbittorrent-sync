# qBitTorrent Sync
Sync qBittorrent data between multiple OS installs.

# Installation:
``` bash
git clone https://github.com/zigai/qbittorrent-sync.git
cd qbittorrent-sync
pip install -r requirements.txt
```
Enable WebUI in qBittorrent: Tools -> Preferences -> Web UI

# Example exported torrent:
``` json
{
    "name": "ubuntu-mate-22.04.1-desktop-amd64.iso",
    "urls": "magnet:?xt=urn:btih:de9bff3b76489706867baa8021d7e3367998ebba&dn=ubuntu-mate-22.04.1-desktop-amd64.iso&tr=https%3a%2f%2ftorrent.ubuntu.com%2fannounce",
    "save_path": "/mnt/e/files/downloads/",
    "category": "",
    "tags": []
}
```
# Usage:


### As CLI:
NOTE: When importing the script will try to convert torrent paths to unix paths by default. You can overwrite this behaviour when using this script as a Python package. 

```
usage: qbittorrent_sync.py [-h] [-host HOST] [-port PORT] [-username USERNAME] [-password PASSWORD] action path

Sync qBittorrent data between multiple OSs

positional arguments:
  action              import/export
  path                File path

options:
  -h, --help          show this help message and exit
  -host HOST          Default: localhost
  -port PORT          Default: 8080
  -username USERNAME  Default: admin
  -password PASSWORD  Default: adminadmin
```

### As Python package:

``` python
from qbittorrent_sync import QbitTorrentSync

def custom_path_transform(path: str) -> str:
    # Custom function for transforming torrent save path when importing
    ...

client = QbitTorrentSync(path_transform_func=custom_path_transform)
client.import_torrents("./torrents.json")
```
# License
[GPLv3](LICENSE)
