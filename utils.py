import json
import config
import strings
import logging
import requests

def get_latest_block():
    return requests.get(f"{config.NXS_BASE_URL}/ledger/list/blocks", params={"limit": 1, "verbose": "detail"}).json()["result"][0]

def get_block(height):
    return requests.get(f"{config.NXS_BASE_URL}/ledger/get/block?verbose=detail&height={height}").json()["result"]

def get_metrics():
    return requests.get(f"{config.NXS_BASE_URL}/system/get/metrics").json()["result"]

def get_mining():
    """Get the mining info"""
    return requests.get(f"{config.NXS_BASE_URL}/ledger/get/info").json()["result"]

def pp(_json):
    print(json.dumps(_json, indent=1))


def load_metrics(filename: str = "metrics.json") -> dict:
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except Exception as e:
        print(e)
        return {}


def save_metrics(metrics: dict):
    with open("metrics.json", "w") as f:
        json.dump(metrics, f)

def extract_contract_info(contract) -> dict:
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

        return {"amount": amount, "op": op, "for": credit_for, "from": tx_from, "proof": proof, "to": tx_to, "token": token, }
    except Exception as e:
        print(e)
        logging.error("Extract contract info error: ", e)

def process_block(block: json, alert_amount: int = config.ALERT_AMOUNT) -> list:
    messages = []
    errors = []
    try:
        for tx in block.get("tx"):
            contracts = tx.get("contracts")
            if contracts is not None:
                for contract in contracts:
                    contract_info = extract_contract_info(contract)
                    amount = contract_info.get("amount")
                    if amount is not None:
                        # todo : this constraint must be removed from here in future
                        if amount >= alert_amount:
                            block_height = block.get("height")
                            message = strings.whale_notification(
                                block_height, contract_info)
                            messages.append(message)
                    else:
                        errors.append(
                            f"contract parsing failed for a contact: {contract} in block: {block.get('height')}")
    except:
        errors.append(f"block parsing failed for {block.get('height')}")
    
    # * log errors
    for error in errors:
        logging.error(error)
    
    return messages
