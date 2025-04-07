import React, { useState } from "react";
import styles from "../styles/Dashboard.module.css";
import Chatbot from "./Chatbot";
import DrugDiscoveryIDE from "./DrugDiscoveryIDE"

// Dummy components for other pages
const MolecularVisualization = () => <div className={styles.pageContent}><h3>3D Molecular Visualization</h3><p> (Comming Soon!)</p></div>;

const Dashboard: React.FC = () => {
  const [isSidebarVisible, setIsSidebarVisible] = useState(true);
  const [activePage, setActivePage] = useState("conversational-ai");

  // Toggle sidebar visibility
  const toggleSidebar = () => {
    setIsSidebarVisible((prev) => !prev);
  };

  // Handle navigation clicks
  const navigateTo = (page: string) => {
    setActivePage(page);
  };

  return (
    <div className={styles.dashboard}>
      {/* Sidebar */}
      <div className={`${styles.sidebar} ${isSidebarVisible ? "" : styles.hidden}`}>
        <button className={styles.toggleButton} onClick={toggleSidebar}>
          {isSidebarVisible ? "Hide Sidebar" : "Show Sidebar"}
        </button>
        <a onClick={() => navigateTo("conversational-ai")}>ChemNova</a>
        <a onClick={() => navigateTo("drug-discovery-ide")}>Drug Discovery IDE</a>
        <a onClick={() => navigateTo("3d-molecular-visualization")}>3D Molecular Visualization</a>
      </div>

      {/* Floating button to show sidebar when hidden */}
      {!isSidebarVisible && (
        <button className={styles.floatingButton} onClick={toggleSidebar}>
          ☰
        </button>
      )}

      {/* Main content area */}
      <div className={`${styles.content} ${isSidebarVisible ? "" : styles.expanded}`}>
        {activePage === "conversational-ai" && <Chatbot />}
        {activePage === "drug-discovery-ide" && <DrugDiscoveryIDE />}
        {activePage === "3d-molecular-visualization" && <MolecularVisualization />}
      </div>
    </div>
  );
};

export default Dashboard;
