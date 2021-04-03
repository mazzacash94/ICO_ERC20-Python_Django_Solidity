const MyToken = artifacts.require("Ico")
const daysLength = "Enter the number of days you want the ico to last without the quotation marks"
module.exports = async function (deployer, network, accounts) {
  // Deploy MyToken
  await deployer.deploy(MyToken, daysLength)
  const myToken = await MyToken.deployed()
}