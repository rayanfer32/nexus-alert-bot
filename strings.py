import config

def remove_none_lines(msg):
    # * remove lines with None values
    _msg = ""
    for line in msg.splitlines():
        if line.find("None") <= -1:
            _msg += line + "\n"
    return _msg


start = "Welcome to nexus alerts bot!"
help = "Use /start to get started"
dead = "Whale notifier process appears dead, please restart the bot."

emojis = {
    "blue_whale": "🐳",
    "whale": "🐋",
    "shark": "🦈",
    "dolphin": "🐬",
    "tuna": "🐟",
    "blowfish": "🐡",
    "sardine": "🐠",
    "octopus1": "🦑",
    "octopus2": "🐙",
    "lobster": "🦞",
    "crab": "🦀",
    "shrimp": "🦐",
}

fish_map = {
    "blue_whale": "Blue Whale",
    "sperm_whale": "Sperm Whale",
    "humpack_whale": "Humpback Whale",
    "whale_shark": "Whale Shark",
    "tiger_shark": "Tiger Shark",
    "blue_white_shark": "Blue White Shark",
    "great_white_shark": "Great White Shark",
    "dolphin": "Dolphin",
    "tuna": "Tuna",
    "sardine": "Sardine",
    "shrimp": "Shrimp"
}


def get_fishname_and_emoji(amount) -> list():
    "get emoji based on amount"
    if amount >= 500000:
        return emojis.get("blue_whale") * 6, fish_map.get("blue_whale")
    elif amount >= 250000:
        return emojis.get("blue_whale") * 6, fish_map.get("sperm_whale")
    elif amount >= 100000:
        return emojis.get("whale") * 3, fish_map.get("humpack_whale")
    elif amount >= 80000:
        return emojis.get("shark") * 6, fish_map.get("whale_shark")
    elif amount >= 60000:
        return emojis.get("shark") * 4, fish_map.get("tiger_shark")
    elif amount >= 30000:
        return emojis.get("shark") * 2, fish_map.get("great_white_shark")
    elif amount >= 10000:
        return emojis.get("dolphin") * 2, fish_map.get("dolphin")
    elif amount >= 5000:
        return emojis.get("tuna") * 2, fish_map.get("tuna")
    elif amount >= 1000:
        return emojis.get("sardine") * 2, fish_map.get("sardine")
    else:
        return emojis.get("shrimp") * 2, fish_map.get("shrimp")


def whale_notification(block_height, contract, tidx, cidx):
    amount = contract.get("amount")
    fish_emoji, fish_name = get_fishname_and_emoji(amount)
    reply_msg = f""" {fish_emoji}
📥 {fish_name} found on Block : `{block_height}`
💰 Amount: `{amount}`
💎 Token: `{contract.get("token")}`
🚦 Operation: `{contract.get("op")}`
☑️ For: `{contract.get("for")}` 
🔗 Proof: `{contract.get("proof")}`
↘️ From: `{contract.get("from")}`
↗️ To: `{contract.get("to")}`
💠 {config.EXPLORER_DOMAIN}/scan/og?block={block_height}&tidx={tidx}&cidx={cidx}"""
    return remove_none_lines(reply_msg)


def info_notification(title, desc):
    return f"ℹ️ {title} ℹ️\n {desc}"

def error_notification(title, desc):
    return f"❗️ {title} ❗️\n {desc}"