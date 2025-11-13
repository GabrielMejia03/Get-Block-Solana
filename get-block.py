import sys
import json
import urllib.request

"""Esto es para la creación de un archivo json"""
def write(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except:
        pass

"""ESe usa el api de solana para obtener el bloque"""
def get_block(slot):
    url = "https://api.mainnet-beta.solana.com"
    payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBlock",
        "params": [
            slot,
            {
                "encoding": "jsonParsed",
                "transactionDetails": "full",
                "rewards": True,
                "maxSupportedTransactionVersion": 0
            }
        ]
    }).encode("utf-8")

    try:
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=20) as res:
            data = json.loads(res.read().decode("utf-8"))
            if "result" in data and data["result"]:
                return data["result"]
    except:
        pass  
    return None

def main():
    args = sys.argv
    slot = None

    if "--block" in args:
        try:
            slot = int(args[args.index("--block") + 1])
        except:
            return

    if not slot:
        return 

    block_data = get_block(slot)
    if block_data:
        write(f"{slot}.json", block_data)

if __name__ == "__main__":
    main()
