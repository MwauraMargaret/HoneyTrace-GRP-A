import { useEffect, useState } from "react";
import { getBatches } from "./services/api.js";
import { getContract } from "./services/contract.js";

function App() {
  const [batches, setBatches] = useState([]);

  useEffect(() => {
    getBatches().then(res => setBatches(res.data));
  }, []);

  async function logContractOwner() {
    const contract = await getContract();
    const owner = await contract.owner();
    console.log("Contract owner:", owner);
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">HoneyTrace Dashboard</h1>
      <button onClick={logContractOwner} className="bg-blue-500 text-white p-2 rounded">
        Check Contract Owner
      </button>
      <ul>
        {batches.map(batch => (
          <li key={batch.id} className="border p-2 my-2">
            {batch.name} – {batch.status}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;