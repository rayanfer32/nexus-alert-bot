from lib2to3.pgen2 import token


start = "Welcome to nexus alerts bot!"
help = "Use /start to get started"

emojis = {'fish1': "🐠", "fish2": "🐟", "fish3": "🐡",
          "shark": "🦈", "whale": "🐋", "blue_whale": "🐳"}

def get_emoji(amount) -> str:
    "get emoji based on amount"
    if amount >= 500000:
        return emojis.get("blue_whale") * 5
    elif amount >= 100000:
        return emojis.get("whale") * 3
    elif amount >= 50000:
        return emojis.get("shark") * 3
    elif amount >= 10000:
        return emojis.get("fish3") * 3
    elif amount >= 5000:
        return emojis.get("fish2") * 3
    else:
        return emojis.get("fish1") * 2

def whale_notification(block_height, contract):
    amount = contract.get("amount")
    return f""" { get_emoji(amount)}  
📥 New Transcation on Block : `{block_height}`
💰 Amount: `{amount}`
💎 Token: `{contract.get("token")}`
🚦 Operation: `{contract.get("op")}`
🔗 Proof: `{contract.get("proof")}`
↘️ From: `{contract.get("from")}`
↗️ To: `{contract.get("to")}`
💠 https://explorer.nexus.io/scan/{block_height}"""
