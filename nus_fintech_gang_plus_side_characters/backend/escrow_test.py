from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import EscrowCreate, EscrowFinish
from xrpl.transaction import submit_and_wait
from xrpl.utils import xrp_to_drops, posix_to_ripple_time
import time

# -----------------------------
# 1. Setup Connection
# -----------------------------
client = JsonRpcClient("https://s.altnet.rippletest.net:51234")

# FIX: Use Wallet.from_seed for reliable derivation
sender = Wallet.from_seed("sEdV9dcBmyzWWHH4Rz3dKZDEjwqGhYQ")
receiver = Wallet.from_seed("sEdTsGN7GAwc1RkH4z4oj7Ei8J9n4sC")

print(f"Donor: {sender.classic_address}")
print(f"Beneficiary: {receiver.classic_address}")

# -----------------------------
# 2. Create the Donation Escrow
# -----------------------------
# We'll set a 'FinishAfter' so the beneficiary can claim it in 10 seconds.
# We MUST convert the Unix time to Ripple Epoch time.
unlock_time_unix = time.time() + 10
ripple_finish_after = posix_to_ripple_time(unlock_time_unix)

escrow_create_tx = EscrowCreate(
    account=sender.classic_address,
    amount=xrp_to_drops(5),
    destination=receiver.classic_address,
    finish_after=ripple_finish_after
)

print("\nStep 1: Submitting Donation to Escrow...")
# submit_and_wait handles the Sequence and Fee for you automatically!
create_res = submit_and_wait(escrow_create_tx, client, sender)

# Get the EXACT sequence number from the result
# print(create_res)
actual_sequence = create_res.result["tx_json"]["Sequence"]
ledger_hash = create_res.result["ledger_hash"]
print(ledger_hash)
print(f"Success! Escrow created with Sequence: {actual_sequence}")

# -----------------------------
# 3. Beneficiary Redemption
# -----------------------------
print(f"\nWaiting 11 seconds for the donation to unlock...")
time.sleep(11)

escrow_finish_tx = EscrowFinish(
    account=receiver.classic_address,
    owner=sender.classic_address,
    offer_sequence=actual_sequence
)

print("Step 2: Beneficiary is redeeming the donation...")
finish_res = submit_and_wait(escrow_finish_tx, client, receiver)

if finish_res.is_successful():
    print("DONE! Funds moved from the Escrow vault to the Beneficiary.")
else:
    print(f"Failed: {finish_res.result['meta']['TransactionResult']}")