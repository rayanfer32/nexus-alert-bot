import json
import time
import dotenv

from utils import get_latest_block
dotenv.load_dotenv()

import config
import strings
import threading 
from pyrogram import Client, filters

import logging
logging.basicConfig(filename="debug.log", format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

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
    message.reply(LAST_BLOCK)


def whale_notifier():
    global LAST_BLOCK

    def scan_new_block(block):
        def find_amount(contract):
            try:
                # ! only handles trituim txns, legacy amount is not included
                amt = contract.get("amount")
                print(f"amount: {amt}")
                return amt
            except Exception as e:
                print(e)
                logging.info(e)


        for tx in block.get("tx"):
            for contract in tx.get("contracts"):
                amt = find_amount(contract)
                if amt is not None:
                    if amt > config.ALERT_AMOUNT:
                        print(f"{amt} > {config.ALERT_AMOUNT}")
                        # * send message to developer
                        block_height = block.get("height")
                        bot.send_message(config.DEVELOPER_CHAT_ID, f"{strings.whale_notification(block_height, amt)}")
                else:
                    logging.error(f"block parsing failed for {block.get('height')}")


    logging.info("Starting whale notifier thread.")
    while True:
        try:
            # * fetch topmost block
            block_json = get_latest_block()
            if block_json["height"] != LAST_BLOCK:
                scan_new_block(block_json)
            else:
                print("no new block")
                logging.info("no new block")
            LAST_BLOCK = block_json["height"]            
        except Exception as e:
            print(e)    
            logging.error(e)
        time.sleep(config.POLLING_INTERVAL) # * wait before next block scan
    logging.error("Thread exited")

if __name__ == "__main__":
    logging.info("Starting bot...")
    LAST_BLOCK = 0
    whale_notifier_thread = threading.Thread(target=lambda: whale_notifier(),daemon = True).start()
    bot.run()
