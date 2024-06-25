import React, { useEffect, useState } from "react";
import { fetchPastas } from "../services/pastaService";
import { Pasta } from "../types/Pasta";
import PastaList from "../components/PastaList";
import { parse } from "path";

const PastaListPage: React.FC = () => {
  const [pastas, setPastas] = useState<Pasta[]>([]);
  const [sortBy, setSortBy] = useState<string>("timestamp");
  const [order, setOrder] = useState<number>(-1);
  const [limit, setLimit] = useState(10); // Default limit
  const [offset, setOffset] = useState(0); // Default offset

  useEffect(() => {
    fetchPastasData();
  }, [sortBy, order, limit, offset]);

  const fetchPastasData = async () => {
    try {
      const data = await fetchPastas(sortBy, order, limit, offset);
      setPastas(data);
    } catch (error) {
      console.error("Error fetching pastas:", error);
    }
  };

  const handleSortChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSortBy(event.target.value);
  };

  const handleOrderChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setOrder(parseInt(event.target.value));
  };

  const handlePastaClick = (pastaId: number) => {
    window.open(`/pasta/${pastaId}`, "_blank");
  };

  const handleLimitChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setOffset(0);
    setLimit(parseInt(event.target.value));
  };

  return (
    <div className="container p-4">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Pasta List</h1>
        <div className="flex space-x-4">
          <select
            className="p-2 rounded bg-black"
            value={sortBy}
            onChange={handleSortChange}
          >
            <option value="timestamp">Date</option>
            <option value="overall_reactions">Reactions</option>
            <option value="author">Author</option>
          </select>
          <select
            className="p-2 border rounded bg-black"
            value={order.toString()}
            onChange={handleOrderChange}
          >
            <option value="-1">Descending</option>
            <option value="1">Ascending</option>
          </select>
          <select
            className="p-2 rounded bg-black"
            value={limit}
            onChange={handleLimitChange}
          >
            <option value="10">10 per page</option>
            <option value="20">20 per page</option>
            <option value="50">50 per page</option>
          </select>
          <button
            className="p-2 rounded bg-gray-400 hover:bg-gray-500 text-white"
            disabled={offset === 0}
            onClick={() => setOffset(offset - limit)}
          >
            Previous Page
          </button>
          <button
            className="p-2 rounded bg-gray-400 hover:bg-gray-500 text-white"
            onClick={() => setOffset(offset + limit)}
          >
            Next Page
          </button>
        </div>
      </div>
      <PastaList pastas={pastas} onPastaClick={handlePastaClick} />
    </div>
  );
};

export default PastaListPage;
