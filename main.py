import json
import time
import dotenv
import strings
import config
import logging
import threading
from pyrogram import Client, filters

from utils import get_block, get_latest_block, process_block
dotenv.load_dotenv()


logging.basicConfig(filename="debug.log", format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

bot = Client(
    config.BOT_NAME,
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)


@bot.on_message(filters.command("start"))
def handle_command(client, message):
    logging.info(message)
    message.reply(strings.start)


@bot.on_message(filters.command("help"))
def handle_command(client, message):
    logging.info(message)
    message.reply(strings.help)


@bot.on_message(filters.command("lastblock"))
def handle_command(client, message):
    logging.info(message)
    message.reply(main_context["last_block"])


@bot.on_message(filters.command("b"))
def handle_command(client, message):
    blocknum: int = message.command[1]
    print(f"/b {blocknum}")
    block_json = get_block(blocknum)
    responses, errors = process_block(block_json, alert_amount=0)
    for m in responses:
        message.reply(m)
    for err in errors:
        message.reply(err)


def whale_notifier(main_context):
    def get_lost_block() -> int:
        "return None if no lost block or block number if block of the lost block"
        try:
            new_block = int(block_json.get("height"))
            old_block = int(main_context.get("last_block"))
            if(new_block - old_block > 1):
                return old_block + 1
            else:
                return None
        except Exception as e:
            print("get_lost_block ERROR: ", e)
        return None

    def get_lost_blocks(old_height: int, new_height: int) -> list[int]:
        "return list of lost blocks"
        if old_height == 0:
            return []
        if (old_height > new_height):
            return []
        return [old_height + i+1 for i in range(new_height - old_height - 1)]

    def scan_and_send_alert(block: json):
        messages ,errors = process_block(block)
        for msg in messages:
            bot.send_message(config.DEVELOPER_CHAT_ID if config.DEBUG_MODE else config.ALERT_CHANNEL_ID, msg)
        for err in errors:
            bot.send_message(config.DEVELOPER_CHAT_ID, err)

    logging.info("Starting whale notifier thread.")
    try:
        while True:
            try:
                # * fetch topmost block
                block_json = get_latest_block()

                # * find if any blocks is lost and send alert
                new_block = int(block_json.get("height"))
                old_block = int(main_context.get("last_block"))
                lost_blocks = get_lost_blocks(old_height=old_block, new_height=new_block)
                for lost_block in lost_blocks:
                    logging.info(
                        f"scanning lost block {lost_block} in whale notifier")
                    scan_and_send_alert(get_block(lost_block))

                if block_json.get("height") != main_context.get("last_block"):
                    scan_and_send_alert(block_json)
                else:
                    print("no new block")
                    logging.info("no new block")
            except Exception as e:
                print(e)
                logging.error(e)

            main_context.update({"last_block": block_json.get("height")})
            # * wait before next block scan
            time.sleep(config.POLLING_INTERVAL)
    except Exception as e:
        logging.error("whale_notifier_thread exited due to error: ", e)


if __name__ == "__main__":
    logging.info("Starting bot...")
    main_context = {"last_block": 0}
    whale_notifier_thread = threading.Thread(
        target=lambda: whale_notifier(main_context), daemon=True)
    whale_notifier_thread.start()
    bot.run()
