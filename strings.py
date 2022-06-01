from typing import List

start = "Welcome to nexus alerts bot!"
help = "Use /start to get started"

emojis = {"blue_whale": "🐳", "whale": "🐋", "shark": "🦈", "dolphin": "🐬", "tuna": "🐟",
          "blowfish": "🐡", "fish1": "🐠", }

fish_map = {"name1": "Blue Whale", "name2": "Sperm Whale", "name3": "Humpback Whale",
            "name4": "Whale Shark", "name5": "Tiger Shark", "name6": "Dolphin", "name7": "Tuna",
            "name8": "Blowfish"}


def get_fishname_and_emoji(amount) -> List[str]:
    "get emoji based on amount"
    if amount >= 500000:
        return emojis.get("blue_whale") * 6, fish_map.get("name1")
    elif amount >= 250000:
        return emojis.get("whale") * 4, fish_map.get("name2")
    elif amount >= 100000:
        return emojis.get("whale") * 2, fish_map.get("name3")
    elif amount >= 80000:
        return emojis.get("shark") * 4, fish_map.get("name4")
    elif amount >= 60000:
        return emojis.get("shark") * 2, fish_map.get("name5")
    elif amount >= 30000:
        return emojis.get("dolphin") * 1, fish_map.get("name6")
    elif amount >= 5000:
        return emojis.get("tuna") * 1, fish_map.get("name7")
    else:
        return emojis.get("blowfish") * 1, fish_map.get("name8")


def whale_notification(block_height, contract):
    amount = contract.get("amount")
    fish_emoji, fish_name = get_fishname_and_emoji(amount)
    return f""" {fish_emoji}
📥 {fish_name} found on Block : `{block_height}`
💰 Amount: `{amount}`
💎 Token: `{contract.get("token")}`
🚦 Operation: `{contract.get("op")}`
☑️ For: `{contract.get("for")}` 
🔗 Proof: `{contract.get("proof")}`
↘️ From: `{contract.get("from")}`
↗️ To: `{contract.get("to")}`
💠 https://explorer.nexus.io/scan/{block_height}"""
