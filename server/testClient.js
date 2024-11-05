// import { io } from "socket.io-client";

// const socket = io("http://localhost:9000"); // 서버 URL에 맞게 설정

// socket.on("connect", () => {
//   console.log("Connected to server");

//   // 서버에 문서 요청
//   const documentId = "1";
//   socket.emit("get-document", documentId);

//   // 서버에서 문서 로드 응답 처리
//   socket.on("load-document", (data) => {
//     console.log("Document loaded from server:", data);

//     // 변경 사항 전송 테스트
//     socket.emit("send-changes", { ops: [{ insert: "Test change\n" }] });
//   });

//   // 서버로부터 변경 사항 수신
//   socket.on("receive-changes", (delta) => {
//     console.log("Received changes from server:", delta);
//   });

//   // 5초 후 문서 저장 테스트
//   setTimeout(() => {
//     socket.emit("save-document", { ops: [{ insert: "Final save\n" }] });
//   }, 5000);
// });

// socket.on("disconnect", () => {
//   console.log("Disconnected from server");
// });