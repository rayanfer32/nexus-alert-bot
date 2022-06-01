import json
import time
import dotenv
import strings
import config
import random
import logging
import threading
from pyrogram import Client, filters

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


@bot.on_message(filters.command("debug"))
def handle_command(client, message):
    logging.info(message)
    message.reply("debug")
    amt = random.randint(0, 1000000)
    msg = strings.whale_notification(main_context.get("last_block"), {
                                     "amount": amt, "op": "CREDIT", "from": "sda", "proof": "das", "to": "sd9a", "token": "NXS"})
    message.reply(msg)


def whale_notifier(main_context):
    # global LAST_BLOCK

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
                credit_for = contract.get("for")
                
                if(op == "DEBIT" and config.HIDE_DEBIT_TXNS):
                    return None
    
                if str(token) in ["0", "0000000000000000000000000000000000000000000000000000000000000000"]:
                    token = "NXS"

                return {"amount": amount, "op": op, "for": credit_for, "from": tx_from, "proof": proof, "to": tx_to, "token": token,}
            except Exception as e:
                print(e)
                logging.info(e)
        try:
            for tx in block.get("tx"):
                contracts = tx.get("contracts")
                if contracts is not None:
                    for contract in contracts:
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
        except:
            logging.error(f"block parsing failed for {block.get('height')}")

    logging.info("Starting whale notifier thread.")
    while True:
        try:
            # * fetch topmost block
            block_json = get_latest_block()
            # * find if any blocks is lost and send alert
            lost_block = get_lost_block()
            if lost_block is not None:
                logging.warning("lost a block in whale notifier")
                scan_and_send_alert(get_block(lost_block))

            if block_json["height"] != main_context["last_block"]:
                scan_and_send_alert(block_json)
            else:
                print("no new block")
                logging.info("no new block")
            main_context["last_block"] = block_json["height"]
        except Exception as e:
            print(e)
            logging.error(e)
            main_context["last_block"] = block_json["height"]
        time.sleep(config.POLLING_INTERVAL)  # * wait before next block scan
    logging.error("Thread exited")


if __name__ == "__main__":
    logging.info("Starting bot...")
    main_context = {"last_block": 0}
    whale_notifier_thread = threading.Thread(
        target=lambda: whale_notifier(main_context), daemon=True).start()
    bot.run()
