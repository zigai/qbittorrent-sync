from pprint import pp, pprint

import pretty_errors
import qbittorrentapi
from stdl import fs
from stdl.str_u import colored


def win_to_unix_path(path: str, drive_path: str = "/mnt"):
    """
    E:\\files\\ -> /mnt/e/files/
    """
    path = path.replace("\\", "/")
    drive = path[0].lower()
    path = path[2:]
    path = f"{drive_path}/{drive}{path}"
    return path


class QbitTorrentDriveSync:

    def __init__(
        self,
        host="localhost",
        port=8080,
        username="admin",
        password="adminadmin",
        path_transoform_func=win_to_unix_path,
    ) -> None:
        self.client = qbittorrentapi.Client(
            host=host,
            port=port,
            username=username,
            password=password,
        )
        self.client.auth_log_in()
        self.path_transoform_func = path_transoform_func

    def get_torrents(self):
        torrents = [dict(**i) for i in self.client.torrents_info()]  # type: ignore
        for i in torrents:
            if i["tags"] == "":
                i["tags"] = []
            else:
                i["tags"] = [i.strip() for i in i["tags"].split(",")]
        return torrents

    def save_torrents(self, path: str):
        torrents = self.get_torrents()
        data = []
        for i in torrents:
            data.append({
                "name": i["name"],
                "urls": i["magnet_uri"],
                "save_path": i["save_path"],
                "category": i["category"],
                "tags": i["tags"],
            })
        fs.json_dump(data, path)
        print(f"{len(data)} torrents saved to {path}.")

    def add_torents(self, path: str):
        current_magets = [i["magnet_uri"] for i in self.get_torrents()]
        data = fs.json_load(path)
        data = [i for i in data if i["urls"] not in current_magets]
        print(f"Adding {len(data)} torrents")
        for i in data:
            name = i["name"]
            del i["name"]
            print(f"Adding '{name}' ... ", end="\r")
            i["save_path"] = self.path_transoform_func(i["save_path"])
            r = self.client.torrents_add(**i) == "Ok."
            print("") if r else print(colored("FAILED", "red"))


def main():
    pass


if __name__ == "__main__":
    main()
