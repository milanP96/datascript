In DeRisk we query historical data from indexers. Store them raw in our database, process them and store the processed data too (current state of the world). The processed data are then visualized and risks are estimated, CTAs are sent out.
For this task there is no need for data storage. Just query the raw data and process them.

1) Get raw data
- to get the raw data use https://starkscan.readme.io/reference/retrieve-events and use address 0x04c0a5193d58f74fbace4b74dcf65481e734ed1714121bdc571da345540efa05 . It is an address of zklend's market smart contract. Do not query all the data, just a sample. Provide comments on how you would query all of the data.

2) Process the data to reconstruct the current state of loans.
- Based on the data in 1) you should be able to construct the current state of loans. Users deposit, withdraw capital, borrow, repay, get liquidated, acquire interest. All should be available in the documentation https://zklend.gitbook.io/documentation/about/portal
- skip the liquidations and the acquiring interest
- assume stationary prices of assets. ETH is worth 2200 USD, wstETH is worth 2200 USD, BTC is worth $40k, DAI USDC and USDT are each worth $1
- The task is to create python class for a loan that has "update state" function(s) and update based on deposit, withdraw, borrow and repay. Additionally add a function calculating health (will be in the zklend docs).
- You might find mismatches between docs and real data. Do not investigate (it would take you too long), just comment on those.

We will review the code and have questions about the implementation and your understanding of the task. Keep in mind this is a simplification otherwise it would take you quite some time to finish this and this task should be done ideally within a day.
If you have any questions, let me and @petrasek.lks@gmail.com know and we will respond.

Best
Marek