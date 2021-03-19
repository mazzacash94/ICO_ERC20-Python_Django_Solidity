const MyToken = artifacts.require("MyToken")

contract("MyToken", async accounts => {
    it("Should deploy smart contract correctly...", async () => {
        let instance = await MyToken.deployed();
        let name = await instance.name();
        let symbol = await instance.symbol();
        assert(name === "Start2Token");
        assert(symbol === "S2T");
    });
    it("Should transfer 1000 tokens to contract creator...", async () => {
        let instance = await MyToken.deployed();
        let balance = await instance.balanceOf(accounts[0]);
        assert(balance == 1000);
    });

    it("Should transfer any amount of tokens correctly to any accounts...", async () => {
        let instance = await MyToken.deployed();
        let randomAccount = accounts[Math.floor(Math.random() * 9) + 1]
        let balance1start = await instance.balanceOf(accounts[0]);
        let balance2start = await instance.balanceOf(randomAccount);
        let amount = Math.floor(Math.random() * 1000) + 1
        assert (balance1start == 1000);
        assert (balance2start == 0);
        await instance.transfer(randomAccount, amount);
        let balance1end = await instance.balanceOf(accounts[0]);
        let balance2end = await instance.balanceOf(randomAccount);
        assert (balance1end == balance1start - amount);
        assert (balance2end == amount);
    });
});