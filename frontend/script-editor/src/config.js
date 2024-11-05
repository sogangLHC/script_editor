// src/config.js
import { createChatBotMessage } from "react-chatbot-kit";

const config = {
  initialMessages: [createChatBotMessage("안녕하세요! 무엇을 도와드릴까요?")],
  botName: "GPT 챗봇",
};

export default config;
