import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchPastaById } from "../services/pastaService";
import { Pasta } from "../types/Pasta";

const PastaDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [pasta, setPasta] = useState<Pasta | null>(null);

  useEffect(() => {
    fetchPastaDetail();
  }, [id]);

  const fetchPastaDetail = async () => {
    if (!id) return;
    try {
      const data = await fetchPastaById(parseInt(id));
      setPasta(data);
    } catch (error) {
      console.error("Error fetching pasta detail:", error);
    }
  };

  return (
    <div className="container mx-auto p-4 text-2xl">
      {pasta ? (
        <div>
          <h1 className="text-4xl font-bold mb-4">
            {pasta.processed_text.title}
          </h1>
          <p>
            {new Date(pasta.processed_text.date_published).toLocaleString()}
          </p>
          <div
            className="mt-4"
            dangerouslySetInnerHTML={{ __html: pasta.processed_text.body }}
          />
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default PastaDetail;
