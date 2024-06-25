import React from "react";
import { Pasta } from "../types/Pasta";
import { Button } from "./ui/button";
import { Card } from "./ui/card";
import { Check } from "lucide-react";

interface PastaCardProps {
  pasta: Pasta;
  onClick: (id: number) => void;
}

const PastaCard: React.FC<PastaCardProps> = ({ pasta, onClick }) => {
  return (
    <div>
      <Card className="p-4 shadow-md rounded-md text-center">
        <h3
          className="text-lg font-bold cursor-pointer"
          onClick={() => onClick(pasta._id)}
        >
          {pasta.processed_text.title || "Untitled"}
        </h3>
        <div className="inline-flex gap-2">
          <p className="text-sm">Reactions: {pasta.overall_reactions}</p>
          <p className="text-sm">Positive ratio: {pasta.ratio}%</p>
        </div>
        <p className="text-sm"></p>
        <div className="inline-flex gap-2">
          <p>Read</p>
          <input type="checkbox"></input>
        </div>
        <p className="text-sm">
          Published:{" "}
          {new Date(pasta.processed_text.date_published).toLocaleString()}
        </p>
      </Card>
    </div>
  );
};

export default PastaCard;
