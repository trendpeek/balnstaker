# balnstaker

BALN staking reward analyzer.

This APP reads Balanced.network smartcontract
to obtain the amount of network fee rewards 
earned.

----
FAQs
----
1) Is Balnstaker safe to use?

  A) It is totally safe to use your public address, balnstaker never ask for your private key.


2) Does it include BALN Liquidity provider reward as well?

  A) Yes, the network rewards displayed are for staking and/or providing liquidity.


3) Does it include BALN Liquidity provider reward as well?

  A) Yes, the network rewards displayed are for staking and/or providing liquidity.


4) How do you calculate the network fee rewards?

  A) We read the divident info by calling getUserDividends(account, start, end) from balanced smart contract for dividents.
     You can find the smart contract below.    

     https://tracker.icon.foundation/contracts/1?count=25&keyword=balanced


5) Do you calculate using daily snapshots, is that correct?

  A) Balnstaker do not calculate the rewards, it just read daily snapshot info from balanced smartcontract. Same as you read price info or APY info by calling smartcontract.
