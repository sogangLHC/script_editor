// import express from "express";
// import { createServer } from "http";
// import { Server } from "socket.io";
// import cors from "cors";
// import dotenv from "dotenv";
// import Connection from "./database/db.js";
// import {
//   getDocument,
//   updateDocument,
// } from "./controllers/documentController.js";

// dotenv.config();

// const PORT = process.env.PORT || 9000;

// Connection();

// const app = express();

// app.use(cors({
//   origin: 'https://lhc-flax.vercel.app', // Ensure this matches your frontend URL
//   methods: ["GET", "POST"], // Allow methods as needed
//   credentials: true // Enable credentials if required
// }));

// const httpserver = createServer(app);

// const io = new Server(httpserver, {
//   cors: {
//     origin: "https://lhc-flax.vercel.app", // Ensure this matches your frontend URL
//     methods: ["GET", "POST"],
//     credentials: true
//   },
// });

// io.on("connection", (socket) => {
//   socket.on("get-document", async (documentId) => {
//     const doc = await getDocument(documentId);
//     socket.join(documentId);
//     socket.emit("load-document", doc.data);
    
//     socket.on("send-changes", (delta) => {
//       socket.broadcast.to(documentId).emit("recieve-changes", delta);
//     });

//     socket.on("save-document", async (data) => {
//       await updateDocument(documentId, data);
//     });
//   });
// });

// httpserver.listen(PORT, () => {
//   console.log(`Server is running on port ${PORT}`);
// });

import express from "express";
import { createServer } from "http";
import { Server } from "socket.io";
import cors from "cors";
import dotenv from "dotenv";
import Connection from "./database/db.js";
import {
  getDocument,
  updateDocument,
} from "./controllers/documentController.js";

dotenv.config();

const PORT = process.env.PORT || 9000;

Connection();

const app = express();

// CORS 설정
app.use(cors({
  origin: 'https://lhc-flax.vercel.app', // 프론트엔드 URL로 업데이트
  methods: ["GET", "POST"],
  credentials: true
}));

const httpserver = createServer(app);

const io = new Server(httpserver, {
  cors: {
    origin: "https://lhc-flax.vercel.app", // 프론트엔드 URL로 업데이트
    methods: ["GET", "POST"],
    credentials: true
  },
});

io.on("connection", (socket) => {
  console.log("A client connected:", socket.id);

  socket.on("get-document", async (documentId) => {
    console.log(`Client requested document: ${documentId}`);
    const doc = await getDocument(documentId);
    socket.join(documentId);
    socket.emit("load-document", doc.data);

    socket.on("send-changes", (delta) => {
      console.log("Received changes from client:", delta);
      socket.broadcast.to(documentId).emit("receive-changes", delta); // "receive"로 오타 수정
    });

    socket.on("save-document", async (data) => {
      console.log("Saving document data:", data);
      await updateDocument(documentId, data);
      console.log("Document saved successfully");
    });
  });

  socket.on("disconnect", () => {
    console.log("Client disconnected:", socket.id);
  });
});

httpserver.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});