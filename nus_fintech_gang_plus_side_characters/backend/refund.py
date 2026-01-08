import requests
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import EscrowCancel
from xrpl.transaction import submit_and_wait

# 1. Configuration
API_URL = "http://127.0.0.1:8000"
client = JsonRpcClient("https://s.altnet.rippletest.net:51234")
donor_wallet = Wallet.from_seed("sEdV9dcBmyzWWHH4Rz3dKZDEjwqGhYQ") 

def get_pending_donations():
    """Ask the API for the list of active donations"""
    try:
        response = requests.get(f"{API_URL}/available_claims")
        return response.json()
    except Exception as e:
        print(f"Error connecting to server: {e}")
        return []

def refund_donation(sequence_num):
    print(f"Attempting to refund Ticket #{sequence_num}...")
    
    # A. Submit to Ledger
    cancel_tx = EscrowCancel(
        account=donor_wallet.classic_address,
        owner=donor_wallet.classic_address,
        offer_sequence=sequence_num
    )

    try:
        response = submit_and_wait(cancel_tx, client, donor_wallet)
        
        if response.is_successful():
            print("✅ Ledger Success: Funds returned to Donor.")
            
            # B. Tell the API to update the DB
            requests.post(f"{API_URL}/mark_refunded/{sequence_num}")
            print("✅ Database Updated: Status set to REFUNDED.")
            
        else:
            print("❌ Ledger Failed:", response.result["meta"]["TransactionResult"])
            print("   (Reason: Has the 'CancelAfter' time passed yet?)")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("--- REFUND DASHBOARD ---")
    items = get_pending_donations()
    
    if not items:
        print("No pending donations found.")
    else:
        for item in items:
            print(f" - Ticket #{item['sequence']} | {item['amount']} XRP")
            
        seq = input("\nEnter Ticket # to Refund: ")
        refund_donation(int(seq))