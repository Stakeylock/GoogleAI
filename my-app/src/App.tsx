// src/App.tsx
import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./components/Dashboard";
import Chatbot from "./components/Chatbot";
import DrugDiscoveryIDE from "./components/DrugDiscoveryIDE";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* The Dashboard as the main layout */}
        <Route path="/" element={<Dashboard />}>
          <Route path="chemnova" element={<Chatbot />} />
          {/* Add the new route for the IDE */}
          <Route path="drug-discovery-ide" element={<DrugDiscoveryIDE />} />
          {/* ...other routes if needed */}
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
