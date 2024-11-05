// import document from "../models/document.js";

// export const getDocument = async (id) => {
//   if (id === null) return;

//   const doc = await document.findById(id);

//   if (doc) return doc;

//   return await document.create({ _id: id, data: "" });
// };

// export const updateDocument = async (id, data) => {
//   return await document.findByIdAndUpdate(id, { data });
// };

import document from "../models/document.js";

export const getDocument = async (id) => {
  if (id === null) return;

  let doc = await document.findById(id);

  if (doc) return doc;

  // 기본 데이터를 빈 Quill 형식으로 생성
  console.log("Document not found. Creating a new document.");
  return await document.create({ _id: id, data: { ops: [] } });
};

export const updateDocument = async (id, data) => {
  console.log("Updating document:", id, data);
  return await document.findByIdAndUpdate(id, { data }, { new: true });
};