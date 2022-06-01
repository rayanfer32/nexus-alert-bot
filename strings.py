from lib2to3.pgen2 import token


start = "Welcome to nexus alerts bot!"
help = "Use /start to get started"

emojis = {"blue_whale": "🐳", "whale": "🐋", "shark": "🦈", "dolphin": "🐬", "tuna": "🐟",
          "blowfish": "🐡", "fish1": "🐠", }

fish_name = {"name1":"Blue Whale", "name2": "Sperm Whale", "name3": "Humpback Whale",
             "name4": "Whale Shark", "name5": "Tiger Shark", "name6": "Dolphin", "name7": "Tuna",
             "name8": "Blowfish"}


def get_emoji(amount) -> str:
    "get emoji based on amount"
    if amount >= 500000:
        return emojis.get("blue_whale") * 6
    elif amount >= 250000:
        return emojis.get("whale") * 4
    elif amount >= 100000:
        return emojis.get("whale") * 2    
    elif amount >= 80000:
        return emojis.get("shark") * 4
    elif amount >= 60000:
        return emojis.get("shark") * 2
    elif amount >= 30000:
        return emojis.get("dolphin") * 1
    elif amount >= 5000:
        return emojis.get("tuna") * 1
    else:
        return emojis.get("blowfish") * 1


def get_fish(amount) -> str:
    "get fish name based on amount"
    if amount >= 500000:
        return fish_name.get("name1")
    elif amount >= 250000:
        return fish_name.get("name2")
    elif amount >= 100000:
        return fish_name.get("name3")
    elif amount >= 80000:
        return fish_name.get("name4")
    elif amount >= 60000:
        return fish_name.get("name5")
    elif amount >= 30000:
        return fish_name.get("name6")
    elif amount >= 5000:
        return fish_name.get("name7")
    else:
        return fish_name.get("name8")
    


def whale_notification(block_height, contract):
    amount = contract.get("amount")
    return f""" {get_emoji(amount)}
📥 {get_fish(amount)} found on Block : `{block_height}`
💰 Amount: `{amount}`
💎 Token: `{contract.get("token")}`
🚦 Operation: `{contract.get("op")}`
☑️  For: `{contract.get("for") }` 
🔗 Proof: `{contract.get("proof")}`
↘️ From: `{contract.get("from")}`
↗️ To: `{contract.get("to")}`
💠 https://explorer.nexus.io/scan/{block_height}"""
