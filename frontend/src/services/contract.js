import { ethers } from "ethers";
import AsaliTrace from "../../contracts/contracts/AsaliTrace.sol/AsaliTrace.json";

// Deployed contract address (replace after deployment)
const contractAddress = "0xYourContractAddress";

export async function getContract() {
  if (!window.ethereum) throw new Error("MetaMask not found");
  
  await window.ethereum.request({ method: "eth_requestAccounts" });
  const provider = new ethers.BrowserProvider(window.ethereum);
  const signer = await provider.getSigner();
  return new ethers.Contract(contractAddress, AsaliTrace.abi, signer);
}