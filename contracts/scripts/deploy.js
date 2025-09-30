import { ethers } from "hardhat";

async function main() {
  const AsaliTrace = await ethers.getContractFactory("AsaliTrace");
  const contract = await AsaliTrace.deploy();
  await contract.waitForDeployment();

  console.log(`AsaliTrace deployed to: ${await contract.getAddress()}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});