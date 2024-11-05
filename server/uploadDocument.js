import mongoose from "mongoose";
import dotenv from "dotenv";
import Document from "./models/document.js";

dotenv.config();

// MongoDB에 연결
const connectToDatabase = async () => {
  try {
    await mongoose.connect(process.env.MONGO_URI, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
    console.log("Connected to MongoDB Atlas");
  } catch (error) {
    console.error("Error connecting to MongoDB:", error);
  }
};

// 새 문서 업로드 함수
const uploadDocument = async (id, data) => {
  try {
    const newDocument = new Document({
      _id: id,     // 문서 ID
      data: data,  // 문서 내용 (객체 형식)
    });

    // 데이터베이스에 문서 저장
    await newDocument.save();
    console.log("Document uploaded successfully:", newDocument);
  } catch (error) {
    console.error("Error uploading document:", error);
  }
};

// MongoDB에 연결 후 문서 업로드 실행
const main = async () => {
  await connectToDatabase();

  // 원하는 ID와 JSON 형식의 내용을 설정
  const documentId = "1";
  const documentContent = {
    ops: [
      { insert: "This is a sample text document.\n" },
      { insert: "Bold text example", attributes: { bold: true } },
    ],
  };

  await uploadDocument(documentId, documentContent);

  // 연결 종료
  mongoose.connection.close();
};

main();