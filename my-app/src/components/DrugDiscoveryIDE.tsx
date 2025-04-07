import React, { useState, useRef, ChangeEvent } from "react";
import Editor from "@monaco-editor/react";
import axios from "axios";
import styles from "../styles/DrugDiscoveryIDE.module.css";

const DrugDiscoveryIDE: React.FC = () => {
  const [code, setCode] = useState(`# Write your Python code here
print('Hello from the Drug Discovery IDE!')

# Example: Get SMILES notation for a compound
# compound_name = "Aspirin"
# print(f"Getting SMILES notation for {compound_name}")
`);
  const [output, setOutput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Run code through the API
  const runCode = async () => {
    setIsLoading(true);
    setOutput("Running code...");
    
    try {
      const response = await axios.post("http://localhost:5000/run-code", { code });
      setOutput(response.data.result);
    } catch (error) {
      console.error("Error running code:", error);
      setOutput("Error: Could not execute code. Make sure the API server is running.");
    } finally {
      setIsLoading(false);
    }
  };

  // File operations
  const handleOpenClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      const fileContent = event.target?.result;
      if (typeof fileContent === "string") {
        setCode(fileContent);
      }
    };
    reader.readAsText(file);
  };

  const handleSaveClick = () => {
    const blob = new Blob([code], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "script.py";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  // Add a sample code template
  const insertChemistryTemplate = () => {
    const template = `# Drug Discovery Script Template
# This will query our model for compound information

compound_name = "Aspirin"  # Change this to your compound of interest

print(f"Analyzing {compound_name}...")
print(f"Looking up structure and properties...")

# In a real implementation, this would call our model API
# Example API call structure:
# response = requests.post("http://api.example.com/predict", 
#                         json={"compound": compound_name})
# results = response.json()
# print(f"SMILES: {results['smiles']}")
# print(f"Properties: {results['properties']}")
`;
    setCode(template);
  };

  return (
    <div className={styles.ideContainer}>
      <header className={styles.ideHeader}>
        <h2>Drug Discovery IDE</h2>
      </header>

      <div className={styles.ideBody}>
        <div className={styles.editorSection}>
          <Editor
            height="100%"
            defaultLanguage="python"
            theme="vs-dark"
            value={code}
            onChange={(value) => setCode(value || "")}
          />
        </div>
        <div className={styles.outputSection}>
          <textarea 
            className={styles.outputConsole} 
            readOnly 
            value={output} 
            placeholder="Output will appear here when you run your code..."
          />
        </div>
      </div>

      <footer className={styles.ideFooter}>
        <div className={styles.buttonGroup}>
          <input
            type="file"
            accept=".py,.txt"
            ref={fileInputRef}
            style={{ display: "none" }}
            onChange={handleFileChange}
          />
          <button onClick={handleOpenClick}>Open</button>
          <button onClick={handleSaveClick}>Save</button>
          <button onClick={insertChemistryTemplate}>Insert Template</button>
          <button onClick={runCode} disabled={isLoading}>
            {isLoading ? "Running..." : "Run"}
          </button>
        </div>
      </footer>
    </div>
  );
};

export default DrugDiscoveryIDE;