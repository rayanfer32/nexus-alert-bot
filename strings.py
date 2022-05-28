from lib2to3.pgen2 import token


start = "Welcome to nexus alerts bot!"
help = "Use /start to get started"


def whale_notification(block_height, contract):
    amount = contract.get("amount")
    return f""" { '🐳' * len(str(int(amount)))}  
🐋 Whale found on Block : `{block_height}`
💰 Amount: `{amount} {contract.get("token")}`
🚦 Operation: `{contract.get("op")}`
🔗 Proof: `{contract.get("proof")}`
🔗 From: `{contract.get("from")}`
🔗 To: `{contract.get("to")}`
https://explorer.nexus.io/scan/{block_height}"""
