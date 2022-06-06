import json
import time
import dotenv
import strings
import config
import logging
import threading
from pyrogram import Client, filters
from datetime import datetime
import schedule
import time

from utils import get_block, get_latest_block, get_metrics, load_metrics, pp, process_block, save_metrics
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
    responses = process_block(block_json, alert_amount=0)
    for m in responses:
        message.reply(m)


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

    def scan_and_send_alert(block: json):
        responses = process_block(block)
        for msg in responses:
            bot.send_message(
                config.DEVELOPER_CHAT_ID if config.DEBUG_MODE else config.ALERT_CHANNEL_ID, msg)

    logging.info("Starting whale notifier thread.")
    while True:
        try:
            # * fetch topmost block
            block_json = get_latest_block()

            # * find if any blocks is lost and send alert
            lost_block = get_lost_block()
            if lost_block is not None:
                logging.warning(
                    f"scanning lost block {lost_block} in whale notifier")
                scan_and_send_alert(get_block(lost_block))

            if block_json.get("height") != main_context.get("last_block"):
                scan_and_send_alert(block_json)
            else:
                print("no new block")
                logging.info("no new block")
            main_context.update({"last_block": block_json.get("height")})
        except Exception as e:
            print(e)
            logging.error(e)
            main_context.update({"last_block": block_json.get("height")})
        time.sleep(config.POLLING_INTERVAL)  # * wait before next block scan
    logging.error("Thread exited")

def metrics_notifier():
    def job():
        prev_metrics:dict = load_metrics()
        new_metrics:dict = get_metrics()
        metrics_trees = ["registers", "trust", "supply", "reserves"]

        def get_change_diff(old:dict, new:dict):
            change_diff = {}
            for k,v in old.items():
                change_diff[k] = new[k] - v
            return change_diff

        select_key = metrics_trees[0]
        old_data = prev_metrics.get(select_key)
        new_data = new_metrics.get(select_key)
        change_diff = get_change_diff(old_data, new_data)

        msg = f"#{select_key.title()} - 24 Hour Change Report\n" 

        def custom_change_text(cdiff, k):
            val = cdiff[k]
            val = round(val,2)
            if val == 0:
                return "No Change"
            elif val > 0:
                return f"+{val}▲"
            else:
                return f"{val}▼"

        for k,v in new_metrics.get(select_key).items():
            msg += f"ℹ️ {k.title()}: {round(v,2)} -> {custom_change_text(change_diff,k)}\n"

        bot.send_message(config.DEVELOPER_CHAT_ID, msg)

        save_metrics()
        # pp(metrics_json)

    schedule.every(0.1).minutes.do(job)
    # ? schedule.every().day.at("10:30").do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    logging.info("Starting bot...")
    main_context = {"last_block": 0}
    whale_notifier_thread = threading.Thread(
        target=lambda: whale_notifier(main_context), daemon=True).start()
    metrics_notifier_thread = threading.Thread(
        target=lambda: metrics_notifier(), daemon=True).start()
    bot.run()
