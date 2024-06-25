import axios from "axios";
import { Pasta } from "../types/Pasta";

const API_URL = "http://localhost:8000";

export const fetchPastas = async (
  sort_by: string = "timestamp",
  order: number = -1,
  limit: number = 20, // Default limit
  offset: number = 0 // Default offset
): Promise<Pasta[]> => {
  const response = await axios.get(`${API_URL}/pastas`, {
    params: { sort_by, order, limit, offset },
  });
  return response.data;
};

export const fetchPastaById = async (id: number): Promise<Pasta> => {
  const response = await axios.get(`${API_URL}/pasta/${id}`);
  return response.data;
};
