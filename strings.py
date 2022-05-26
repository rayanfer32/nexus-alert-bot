from lib2to3.pgen2 import token


start = "Welcome to nexus alerts bot!"
help = "Use /start to get started"

def whale_notification(block_height, amount, tx_from="", tx_to="", token="NXS"):
  return f"""New whale transaction on Block : {block_height}
Token: {token}
Amount: {amount}
From: {tx_from}
To: {tx_to}
explorer.nexus.io/scan/{block_height}"""