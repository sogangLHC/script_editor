// src/config.js
import { createChatBotMessage } from "react-chatbot-kit";

const config = {
  initialMessages: [
    createChatBotMessage("저는 문법 오류를 전담해서 수정해드릴게요! 😊"),
  ],
  botName: "Grammar Checker",

  // 특정 스타일만 설정 가능
  customStyles: {
    botMessageBox: {
      backgroundColor: "#e1f5fe", // 봇 메시지 배경색
      color: "#333", // 봇 메시지 텍스트 색상
    },
    chatButton: {
      backgroundColor: "#5ccc9d", // 전송 버튼 색상
    },
  },
};


export default config;
