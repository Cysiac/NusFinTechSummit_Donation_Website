"use client";

import { useState } from "react";
import { xrpToDrops } from "xrpl";
import { useWallet } from "./providers/WalletProvider";

export default function DonateButton() {
  const { walletManager, isConnected, showStatus, addEvent } = useWallet();
  const [isLoading, setIsLoading] = useState(false);

  const donate = async () => {
    if (!isConnected || !walletManager || !walletManager.account) {
      showStatus("Please connect a wallet first", "error");
      return;
    }

    try {
      setIsLoading(true);

      const transaction = {
        TransactionType: "EscrowCreate",
        Account: walletManager.account.address,
        Amount: xrpToDrops(2),
        Destination: "rPEaR2FGwGgi2S5MFVZqzi4SomsRhhw65H",
        FinishAfter: Math.floor(Date.now() / 1000) - 946684800 + 10,
      };

      const txResult = await walletManager.signAndSubmit(transaction);

      showStatus("Donation escrow created successfully!", "success");
      addEvent("Donation Escrow Created", txResult);

      // Notify backend
      const payload = {
        sequence: parseInt(txResult.id, 10),
        tx_hash: txResult.hash ?? "",
        sender: walletManager.account.address ?? "",
        amount: parseFloat(2),
      };

      await fetch("http://localhost:8000/register_donation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          tx_hash: txResult.hash,
          sender: walletManager.account.address,
          amount: 2,
        }),
      });
      
    } catch (error) {
      showStatus(`Donation failed: ${error.message}`, "error");
      addEvent("Donation Failed", error);
    } finally {
      setIsLoading(false);
    }
  };

  if (!isConnected) {
    return null; // same behavior as TransactionForm
  }

  return (
    <button
      onClick={donate}
      disabled={isLoading}
      className="px-4 py-2 bg-accent text-white rounded-lg font-semibold hover:bg-accent/90 disabled:bg-gray-400"
    >
      {isLoading ? "Creating Escrow..." : "Donate 2 XRP"}
    </button>
  );
}
