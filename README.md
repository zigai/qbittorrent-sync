# qBitTorrent Sync
Sync qBitTorrent information between various operating system installations.

## Installation
``` bash
git clone https://github.com/zigai/qbittorrent-sync.git
cd qbittorrent-sync
pip install -r requirements.txt
```
Make sure to enable the WebUI in qBittorrent by going to ```Tools -> Preferences -> Web UI```.

## Example exported torrent:
``` json
{
    "name": "ubuntu-mate-22.04.1-desktop-amd64.iso",
    "urls": "magnet:?xt=urn:btih:de9bff3b76489706867baa8021d7e3367998ebba&dn=ubuntu-mate-22.04.1-desktop-amd64.iso&tr=https%3a%2f%2ftorrent.ubuntu.com%2fannounce",
    "save_path": "/mnt/e/files/downloads/",
    "category": "",
    "tags": []
}
```
## Usage


### As a Command Line Interface
**NOTE**:
The script will attempt to convert torrent paths from Windows to Unix paths by default. It will map Windows drives to /mnt/. ``` eg. "D:\folder\file.torrent" to "/mnt/d/folder/file.torrent" ```.
This can be changed by using the script as a Python package and defining a custom function to transform paths.

```
usage: qbittorrent_sync.py [-h] [-host HOST] [-port PORT] [-username USERNAME] [-password PASSWORD] action path

Sync qBitTorrent information between various operating system installations.

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

### As Python package

``` python
from qbittorrent_sync import QbitTorrentSync

def custom_path_func(path: str) -> str:
    # Custom function for transforming torrent save path when importing
    ...

client = QbitTorrentSync(path_transform_func=custom_path_func)
client.import_torrents("./torrents.json")
```
## License
[GPLv3](LICENSE)
