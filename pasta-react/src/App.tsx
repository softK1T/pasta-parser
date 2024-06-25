import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import PastaListPage from "./pages/PastaListPage";
import PastaDetail from "./pages/PastaDetail";

const App: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<PastaListPage />} />
      <Route path="/pasta/:id" element={<PastaDetail />} />
    </Routes>
  );
};

export default App;
