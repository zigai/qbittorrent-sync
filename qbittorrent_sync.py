import qbittorrentapi
from stdl import fs
from stdl.st import colored


def is_windows_path(path: str):
    return ":" in path and "\\" in path


def win_to_unix_path(path: str, drive_path: str = "/mnt"):
    """
    E:\\files\\ -> /mnt/e/files/
    /mnt/e/files/ -> /mnt/e/files/
    """
    if not is_windows_path(path):
        return path
    path = path.replace("\\", "/")
    drive = path[0].lower()
    path = path[2:]
    path = f"{drive_path}/{drive}{path}"
    return path


def unix_to_win_path(path: str, drive_path: str = "/mnt"):
    """
    /mnt/e/files/ -> E:\\files\\
    """
    path = path.replace(drive_path, "").replace("/", "\\")
    drive = path[1].capitalize()
    path = path[2:]
    path = f"{drive}:{path}"
    return path


def same_path(path: str):
    return path


class QbitTorrentSync:
    def __init__(
        self,
        host="localhost",
        port=8080,
        username="admin",
        password="adminadmin",
        path_transform_func=win_to_unix_path,
    ) -> None:
        self.client = qbittorrentapi.Client(
            host=host,
            port=port,
            username=username,
            password=password,
        )
        self.client.auth_log_in()
        self.path_transoform_func = path_transform_func

    def get_torrents(self):
        torrents = [dict(**i) for i in self.client.torrents_info()]  # type: ignore
        for i in torrents:
            if i["tags"] == "":
                i["tags"] = []
            else:
                i["tags"] = [i.strip() for i in i["tags"].split(",")]
        return torrents

    def export_torrents(self, path: str):
        torrents = self.get_torrents()
        data = []
        for i in torrents:
            data.append(
                {
                    "name": i["name"],
                    "urls": i["magnet_uri"],
                    "save_path": i["save_path"],
                    "category": i["category"],
                    "tags": i["tags"],
                }
            )
        fs.json_dump(data, path)
        print(f"{len(data)} torrents saved to {path}.")

    def import_torrents(self, path: str):
        current = [i["magnet_uri"] for i in self.get_torrents()]
        fs.ensure_paths_exist(path)
        data = fs.json_load(path)
        data = [i for i in data if i["urls"] not in current]
        print(f"Adding {len(data)} torrents ...")
        for i in data:
            name = i["name"]
            del i["name"]
            print(f"Adding '{name}' ... ", end="\r")
            i["save_path"] = self.path_transoform_func(i["save_path"])
            r = self.client.torrents_add(**i) == "Ok."
            print("") if r else print(colored("FAILED", "red"))


def main():
    import argparse

    ap = argparse.ArgumentParser(
        description="Sync qBitTorrent information between various operating system installations."
    )
    ap.add_argument("action", type=str, help="import/export")
    ap.add_argument("path", type=str, help="File path")

    ap.add_argument("-host", type=str, default="localhost", help="Default: localhost")
    ap.add_argument("-port", type=int, default=8080, help="Default: 8080")
    ap.add_argument("-username", type=str, default="admin", help="Default: admin")
    ap.add_argument(
        "-password", type=str, default="adminadmin", help="Default: adminadmin"
    )

    args = ap.parse_args()
    if args.action not in ["import", "export"]:
        print(f"ERROR: Unsupported action '{args.action}'")
        exit(1)
    client = QbitTorrentSync(args.host, args.port, args.username, args.password)
    if args.action == "import":
        client.import_torrents(args.path)
    else:
        client.export_torrents(args.path)


if __name__ == "__main__":
    main()
