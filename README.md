Ethereum Web3 Project for BlockChain Development Course on Start2Impact.

Steps:

- clone the repository;
- install requirements.txt;
- download ganache GUI and run it, copy the privatekey of the first account and replace the string of the variable privateKey in page/utils.py; 
- enter the amount of days you want your ico to last in truffle/migrations/2_deploy_Tokens.js (variable daysLength);
- run in order truffle test, compile and migrate;
- run python manage.py makemigrations and migrate;
- run python manage.py runserver;
- create superuser;
- register an account;
- login;
- add ganache network to metamask (name : Ganache, rpc url : http://127.0.0.1:7545, chain id : 1337);
- login with the superuser and click on the button in the navbar "Hello, Admin" to access the panel to start the sale;
- register an account and login;
- connect from the button in the about section;
- get ether from the faucet page accessing in the about section or import ganache accounts to metamask;
- go to purchase section, click on buy and complete the transaction in the metamask window (or send ether directly from the wallet thanks to the fallback function in the contract, specify gas price to 2e-7 and gaslimit to 100000 if you get error);
- if transaction is was succesful it will appear a button with the hash of transaction which save it in a model by clicking;
- balance (accessing by clicking on username in the navbar) and token availability will be update automatically;
- transaction ids are serialized and visible in the Api Root of Rest Framework typing '/list' after the URL (if '127.0.0.1' > '127.0.0.1/list') or clicking on the relative button in the about section;
- if you want to stop, resume or end sale access the panel from the superuser account;
- the sale will end or at the end of the days selected at the deploy or manually from the admin panel;
- purchase section will be automatically change to transfer section and accessible by the button in the navbar;
- enter the recipient address, amount of tokens and destination address to move them;
- enjoy!
