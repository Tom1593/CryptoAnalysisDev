CREATE TABLE IF NOT EXISTS Transaction_Wallet (
  txn_id INT NOT NULL,
  wallet_id INT NOT NULL,
  ts INT DEFAULT NULL,  -- Optional: Timestamp of the association
  FOREIGN KEY (txn_id) REFERENCES transactions(id),
  FOREIGN KEY (wallet_id) REFERENCES wallets(id),
  UNIQUE (txn_id, wallet_id)  -- Ensures a single transaction cannot be associated with the same wallet multiple times
);
