import threading
import logging
from pyrogram import Client, filters
import strings
import config
import json
import time
import dotenv

from utils import get_block, get_latest_block
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


def whale_notifier(main_context):
    # global LAST_BLOCK

    def scan_and_send_alert(block):
        def extract_info(contract):
            try:
                # ! only handles trituim txns, legacy amount is not included
                amount = contract.get("amount")
                token = contract.get("token")
                tx_from = contract.get("from")
                tx_to = contract.get("to")
                proof = contract.get("proof")
                op = contract.get("OP")
                if str(token) in ["0", "0000000000000000000000000000000000000000000000000000000000000000"]:
                    token = "NXS"
                return {"amount": amount, "op": op, "from": tx_from, "proof": proof, "to": tx_to, "token": token}
            except Exception as e:
                print(e)
                logging.info(e)

        for tx in block.get("tx"):
            for contract in tx.get("contracts"):
                contract_info = extract_info(contract)
                amount = contract_info.get("amount")
                if amount is not None:
                    if amount > config.ALERT_AMOUNT:
                        block_height = block.get("height")
                        message = strings.whale_notification(
                            block_height, contract_info)
                        bot.send_message(
                            config.DEVELOPER_CHAT_ID if config.DEBUG_MODE else config.ALERT_CHANNEL_ID, message)
                else:
                    logging.error(
                        f"block parsing failed for {block.get('height')}")

    logging.info("Starting whale notifier thread.")
    while True:
        try:
            # * fetch topmost block
            block_json = get_latest_block()

            # * find if any blocks is lost and send alert
            try:
                if(int(block_json["height"]) - int(main_context["last_block"]) > 1):
                    logging.warning("lost a block in whale notifier")
                    scan_and_send_alert(
                        get_block(int(main_context["last_block"]) + 1))
            except:
                logging.warning("first block in whale notifier")
                pass

            if block_json["height"] != main_context["last_block"]:
                scan_and_send_alert(block_json)
            else:
                print("no new block")
                logging.info("no new block")
            main_context["last_block"] = block_json["height"]
        except Exception as e:
            print(e)
            logging.error(e)
        time.sleep(config.POLLING_INTERVAL)  # * wait before next block scan
    logging.error("Thread exited")


if __name__ == "__main__":
    logging.info("Starting bot...")
    main_context = {"last_block": 0}
    whale_notifier_thread = threading.Thread(
        target=lambda: whale_notifier(main_context), daemon=True).start()
    bot.run()
