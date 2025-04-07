import React, { useState, KeyboardEvent } from "react";
import axios from "axios";
import styles from "../styles/Chatbot.module.css";
import chemnovaLogo1 from "../assets/chemnova_logo1.png";
import chemnovaLogo from "../assets/chemnova_logo.png";
import youLogo from "../assets/you_logo.png";

const Chatbot: React.FC = () => {
  const [messages, setMessages] = useState<{ text: string; sender: string }[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  // Send message function
  const handleSendMessage = async () => {
    if (!input.trim()) return;
    const newMessages = [...messages, { text: input, sender: "user" }];
    setMessages(newMessages);
    setInput("");
    setLoading(true);

    try {
      const response = await axios.post("http://localhost:5000/chat", { message: input });
      const botMessage = { text: response.data.message, sender: "bot" };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (error) {
      console.error("Error:", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: "Sorry, there was an error.", sender: "bot" },
      ]);
    } finally {
      setLoading(false);
    }
  };

  // Keydown event handler for Enter
  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleSendMessage();
    }
  };

  return (
    <div className={styles.chatContainer}>
      <div className={styles.header}>
        <h2>
          <img className={styles.headimage} src={chemnovaLogo1} alt="ChemNova Logo" />
          ChemNova
        </h2>
      </div>
      <div className={styles.messages}>
        {messages.map((msg, index) => (
          <div key={index} className={msg.sender === "user" ? styles.userMessage : styles.botMessage}>
            <img
              src={msg.sender === "user" ? youLogo : chemnovaLogo}
              alt="Profile"
              className={styles.profilePic}
            />
            <div className={styles.text}>{msg.text}</div>
          </div>
        ))}
        {loading && <div className={styles.loading}>Generating...</div>}
      </div>
      <div className={styles.inputContainer}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          onKeyDown={handleKeyDown}  // <--- Here is the keydown handler
        />
        <button onClick={handleSendMessage} disabled={loading}>
          Send
        </button>
      </div>
    </div>
  );
};

export default Chatbot;
