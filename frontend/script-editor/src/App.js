// src/App.js
import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Chatbot from "react-chatbot-kit";
import "react-chatbot-kit/build/main.css";
import config from "./config";
import MessageParser from "./MessageParser";
import ActionProvider from "./ActionProvider";
import Login from "./components/Login";
import Editor from "./components/Editor";
import "./App.css";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem("access_token"));

  const handleLoginSuccess = () => {
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setIsLoggedIn(false);
  };

  return (
    <Router>
      <Routes>
        {/* 로그인 페이지 */}
        <Route
          path="/login"
          element={
            isLoggedIn ? (
              <Navigate to="/tutoring" />
            ) : (
              <Login onLoginSuccess={handleLoginSuccess} />
            )
          }
        />

        {/* /tutoring 페이지에 챗봇과 공동편집기 렌더링 */}
        <Route
          path="/tutoring"
          element={
            isLoggedIn ? (
              <div style={styles.pageContainer}>
                {/* 좌측 상단의 로그아웃 버튼 */}
                <button onClick={handleLogout} style={styles.logoutButton}>
                  로그아웃
                </button>

                {/* 좌측: 챗봇 영역 (화면의 3분의 1 차지) */}
                <div style={styles.chatbotContainer}>
                  <Chatbot
                    config={config}
                    messageParser={MessageParser}
                    actionProvider={ActionProvider}
                  />
                </div>

                {/* 우측: 공동 편집기 영역 (화면의 3분의 2 차지) */}
                <div style={styles.editorContainer}>
                  <Editor />
                </div>
              </div>
            ) : (
              <Navigate to="/login" />
            )
          }
        />

        {/* 루트 경로 리디렉션 */}
        <Route path="/" element={<Navigate replace to="/login" />} />

        {/* 잘못된 경로는 로그인 페이지로 이동 */}
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

// 스타일 객체 정의
const styles = {
  pageContainer: {
    display: "flex",
    flexDirection: "row",
    height: "100vh",
    position: "relative", // 로그아웃 버튼 위치 지정에 필요
  },
  logoutButton: {
    position: "absolute",
    top: "10px",
    left: "10px",
    padding: "8px 16px",
    fontSize: "14px",
    backgroundColor: "#ff5c5c",
    color: "#fff",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
    zIndex: 1, // 로그아웃 버튼이 다른 요소 위에 표시되도록 설정
  },
  chatbotContainer: {
    flex: 1, // 페이지의 3분의 1 차지
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    padding: "20px",
    backgroundColor: "#fff",
    boxShadow: "2px 0px 10px rgba(0, 0, 0, 0.1)",
    height: "100vh",
    overflowY: "auto",
  },
  editorContainer: {
    flex: 1.5, // 페이지의 3분의 2 차지
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    padding: "20px",
    backgroundColor: "#f5f5f5",
    height: "100vh",
    overflowY: "auto",
  },
};

export default App;
