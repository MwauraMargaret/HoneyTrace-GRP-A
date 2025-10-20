import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000/api", // Django backend
});

export const getBatches = () => API.get("/batches/");
export const createBatch = (data) => API.post("/batches/", data);