// src/App.js
import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Chatbot from "react-chatbot-kit";
import "react-chatbot-kit/build/main.css";
import config from "./config";
import MessageParser from "./MessageParser";
import ActionProvider from "./ActionProvider";
import Login from "./components/Login";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem("access_token"));

  const handleLoginSuccess = () => {
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    // 로그아웃 처리: 토큰 삭제 및 로그인 상태 갱신
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setIsLoggedIn(false);
  };

  return (
    <Router>
      <Routes>
        <Route
          path="/login"
          element={isLoggedIn ? <Navigate to="/chatbot" /> : <Login onLoginSuccess={handleLoginSuccess} />}
        />
        <Route
          path="/chatbot"
          element={
            isLoggedIn ? (
              <div style={styles.chatbotContainer}>
                <div style={styles.header}>
                  <button onClick={handleLogout} style={styles.logoutButton}>
                    로그아웃
                  </button>
                </div>
                <div style={styles.chatbot}>
                  <Chatbot
                    config={config}
                    messageParser={MessageParser}
                    actionProvider={ActionProvider}
                  />
                </div>
              </div>
            ) : (
              <Navigate to="/login" />
            )
          }
        />
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

const styles = {
  chatbotContainer: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    height: "100vh",
    backgroundColor: "#f0f0f0",
    justifyContent: "center",
  },
  header: {
    width: "100%",
    display: "flex",
    justifyContent: "flex-end",
    padding: "10px",
    position: "absolute",
    top: 0,
    right: 0,
  },
  logoutButton: {
    padding: "8px 16px",
    fontSize: "16px",
    backgroundColor: "#ff5c5c",
    color: "#fff",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
  },
  chatbot: {
    width: "500px",
    height: "600px",
    boxShadow: "0px 4px 12px rgba(0, 0, 0, 0.1)",
    borderRadius: "10px",
    overflow: "hidden",
    position: "relative",
  },
};

export default App;
