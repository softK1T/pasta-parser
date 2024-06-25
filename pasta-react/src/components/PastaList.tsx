import React from "react";
import { Pasta } from "../types/Pasta";
import PastaCard from "./PastaCard";

interface PastaListProps {
  pastas: Pasta[];
  onPastaClick: (id: number) => void;
}

const PastaList: React.FC<PastaListProps> = ({ pastas, onPastaClick }) => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
      {pastas.map((pasta) => (
        <PastaCard key={pasta._id} pasta={pasta} onClick={onPastaClick} />
      ))}
    </div>
  );
};

export default PastaList;
