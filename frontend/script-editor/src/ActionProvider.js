// src/ActionProvider.js
import axios from "axios";

class ActionProvider {
  constructor(createChatBotMessage, setStateFunc) {
    this.createChatBotMessage = createChatBotMessage;
    this.setState = setStateFunc;
  }

  async getAnswerFromAPI(userText) {
    try {
      const token = localStorage.getItem("access_token"); // 저장된 토큰 가져오기
      console.log("토큰:", token);

      // Django 백엔드 API에 userText를 전송하여 처리 결과를 가져옴
      const response = await axios.post(
        "http://localhost:8000/api/process-user-text/",
        { text: userText },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const correctedText = response.data.corrected_text; // 수정된 텍스트 가져오기

      // 챗봇에 보여줄 응답 형식 설정
      const botMessage = this.createChatBotMessage(`수정된 문장: ${correctedText}`);
      
      // 상태 업데이트하여 챗봇 메시지 표시
      this.setState((prev) => ({
        ...prev,
        messages: [...prev.messages, botMessage],
      }));
    } catch (error) {
      console.error("API 요청 중 오류 발생:", error);
      const errorMessage = this.createChatBotMessage("죄송합니다. 응답을 가져오는 중 오류가 발생했습니다.");
      this.setState((prev) => ({
        ...prev,  
        messages: [...prev.messages, errorMessage],
      }));
    }
  }
}

export default ActionProvider;
