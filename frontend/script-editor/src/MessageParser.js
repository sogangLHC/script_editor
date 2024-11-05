// MessageParser.js
class MessageParser {
  constructor(actionProvider) {
    this.actionProvider = actionProvider;
  }

  parse(message) {
    if (message.trim()) {
      // 질문이 있을 때만 API 호출
      this.actionProvider.getAnswerFromAPI(message);
    }
  }
}

export default MessageParser;
