from datetime import datetime
import os
import httpx
from hyperliquid.info import Info
from hyperliquid.utils.types import UserFillsSubscription, UserFillsMsg


def notify(msg: str):
    httpx.post(os.getenv("DISCORD_WEBHOOK_URL"), json={"content": msg})


def cb(msg: UserFillsMsg):
    if "isSnapshot" in msg["data"] and msg["data"]["isSnapshot"]:
        return

    fills = msg["data"]["fills"]
    content = ""
    for fill in fills:
        dt = datetime.fromtimestamp(fill["time"] / 1000)
        content += f"{dt.strftime('%Y-%m-%d %H:%M:%S')} {fill['coin']} {fill['sz']} {fill['startPosition']} {fill['dir']}\n"
    print(content)
    notify(content)


def main():
    info = Info()

    sub: UserFillsSubscription = {
        "type": "userFills",
        "user": os.getenv("HYPERLIQUID_ADDRESS"),
    }
    info.subscribe(sub, cb)


if __name__ == "__main__":
    main()
