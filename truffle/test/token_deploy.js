const MyToken = artifacts.require("Ico")

contract("Ico", async accounts => {
    it("Should deploy smart contract correctly...", async () => {
        let instance = await MyToken.deployed();
        let name = await instance.name();
        let symbol = await instance.symbol();
        assert (name === "Start2Token");
        assert (symbol === "S2T");
    });
    it("Should transfer 1000 tokens to contract creator...", async () => {
        let instance = await MyToken.deployed();
        let balance = await instance.balanceOf(accounts[0]);
        assert (balance == 1000);
    });