// src/ActionProvider.js
import axios from "axios";

class ActionProvider {
  constructor(createChatBotMessage, setStateFunc) {
    this.createChatBotMessage = createChatBotMessage;
    this.setState = setStateFunc;
  }

  async getAnswerFromAPI(question) {
    try {
      const token = localStorage.getItem("access_token");  // 저장된 토큰 가져오기
      console.log(token);
      const response = await axios.post(
        "http://localhost:8000/api/edit-script/",
        { question },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const answer = response.data.answer;
      const explanation = response.data.explanation;

      // 챗봇에 보여줄 응답 형식 설정
      const botMessage = this.createChatBotMessage(`Answer: ${answer}\nExplanation: ${explanation}`);
      
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