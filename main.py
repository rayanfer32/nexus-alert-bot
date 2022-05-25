import json
import time
import dotenv
dotenv.load_dotenv()

import requests
import config
import strings
from threading import Thread
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


def whale_notifier():
    

    def pp(_json):
        json.dumps(_json, indent=1)


    def get_latest_block():
        return requests.get(f"{config.NXS_BASE_URL}/ledger/list/blocks", params={"limit":1, "verbose":"detail"}).json()["result"][0]

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
                if amt is None:
                    logging.error(f"block parsing failed for {block.get('height')}")
                if amt > config.ALERT_AMOUNT:
                    print(f"{amt} > {config.ALERT_AMOUNT}")
                    # * send message to developer
                    bot.send_message(config.DEVELOPER_CHAT_ID, f"{amt} Nxs in a block! explorer.nexus.io/scan/{block.get('height')}")

    last_block = 0

    logging.info("Starting whale notifier thread.")
    while True:
        try:
            # * fetch topmost block
            block_json = get_latest_block()
            if block_json["height"] != last_block:
                scan_new_block(block_json)
            else:
                print("no new block")
                logging.info("no new block")
            last_block = block_json["height"]            
        except Exception as e:
            print(e)    
            logging.error(e)
        time.sleep(config.POLLING_INTERVAL) # * wait before next block scan


logging.info("Starting bot...")
Thread(target=lambda: whale_notifier(),daemon = True).start()
bot.run()
