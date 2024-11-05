// import React, { useEffect, useState } from "react";
// import Quill from "quill";
// import "quill/dist/quill.snow.css";

// import { Box } from "@mui/material";
// import styled from "@emotion/styled";
// import { io } from "socket.io-client";
// import { useParams } from "react-router-dom";

// const Component = styled.div`
//   background: #f5f5f5;
// `;

// const toolbarOptions = [
//   ["bold", "italic", "underline", "strike"], // toggled buttons
//   ["blockquote", "code-block"],

//   [{ header: 1 }, { header: 2 }], // custom button values
//   [{ list: "ordered" }, { list: "bullet" }],
//   [{ script: "sub" }, { script: "super" }], // superscript/subscript
//   [{ indent: "-1" }, { indent: "+1" }], // outdent/indent
//   [{ direction: "rtl" }], // text direction

//   [{ size: ["small", false, "large", "huge"] }], // custom dropdown
//   [{ header: [1, 2, 3, 4, 5, 6, false] }],

//   [{ color: [] }, { background: [] }], // dropdown with defaults from theme
//   [{ font: [] }],
//   [{ align: [] }],

//   ["clean"], // remove formatting button
// ];
// const Editor = () => {
//   const [quill, setQuill] = useState();
//   const [socket, setSocket] = useState();
//   const { id } = useParams();

//   useEffect(() => {
//     const quillServer = new Quill("#container", {
//       theme: "snow",
//       modules: { toolbar: toolbarOptions },
//     });
//     quillServer.disable();
//     quillServer.setText("Loading the document");
//     setQuill(quillServer);
//   }, []);
//   useEffect(() => {
//     const socketServer = io(process.env.REACT_APP_API_URL || "http://localhost:9000");
//     setSocket(socketServer);
  
//     socketServer.on("connect", () => {
//       console.log("Connected to socket server");
//     });
  
//     socketServer.on("disconnect", () => {
//       console.log("Disconnected from socket server");
//     });
  
//     return () => {
//       socketServer.disconnect();
//     };
//   }, []);

//   useEffect(() => {
//     if (socket === null || quill === null) return;

//     const handelChange = (delta, oldData, source) => {
//       if (source !== "user") return;
//       socket && socket.emit("send-changes", delta);
//     };

//     quill && quill.on("text-change", handelChange);

//     return () => {
//       quill && quill.off("text-change", handelChange);
//     };
//   }, [quill, socket]);

//   useEffect(() => {
//     if (socket === null || quill === null) return;

//     const handelChange = (delta) => {
//       quill.updateContents(delta);
//     };
//     socket && socket.on("receive-changes", handelChange);

//     return () => {
//       socket && socket.off("receive-changes", handelChange);
//     };
//   }, [quill, socket]);

//   useEffect(() => {
//     if (quill === null || socket === null) return;

//     socket &&
//       socket.once("load-document", (document) => {
//         quill && quill.setContents(document);
//         quill && quill.enable();
//       });

//     socket && socket.emit("get-document", id);
//   }, [quill, socket, id]);

//   useEffect(() => {
//     if (socket == null || socket == null) return;

//     const interval = setInterval(() => {
//       socket && socket.emit("save-document", quill.getContents());
//     }, 2000);

//     return () => {
//       clearInterval(interval);
//     };
//   }, [socket, quill]);

//   return (
//     <Component>
//       <Box className="container" id="container"></Box>
//     </Component>
//   );
// };

// export default Editor;

import React, { useEffect, useState } from "react";
import Quill from "quill";
import "quill/dist/quill.snow.css";

import { Box } from "@mui/material";
import styled from "@emotion/styled";
import { io } from "socket.io-client";
import { useParams } from "react-router-dom";

const Component = styled.div`
  background: #f5f5f5;
`;

const toolbarOptions = [
  ["bold", "italic", "underline", "strike"],
  ["blockquote", "code-block"],
  [{ header: 1 }, { header: 2 }],
  [{ list: "ordered" }, { list: "bullet" }],
  [{ script: "sub" }, { script: "super" }],
  [{ indent: "-1" }, { indent: "+1" }],
  [{ direction: "rtl" }],
  [{ size: ["small", false, "large", "huge"] }],
  [{ header: [1, 2, 3, 4, 5, 6, false] }],
  [{ color: [] }, { background: [] }],
  [{ font: [] }],
  [{ align: [] }],
  ["clean"],
];

const Editor = () => {
  const [quill, setQuill] = useState();
  const [socket, setSocket] = useState();
  const { id } = useParams();

  useEffect(() => {
    const quillServer = new Quill("#container", {
      theme: "snow",
      modules: { toolbar: toolbarOptions },
    });
    quillServer.disable();
    quillServer.setText("Loading the document...");
    setQuill(quillServer);
  }, []);

  useEffect(() => {
    const socketServer = io(process.env.REACT_APP_API_URL || "http://localhost:9000", {
      transports: ["websocket"], // WebSocket 강제 사용
    });
    setSocket(socketServer);

    console.log("Attempting to connect to:", process.env.REACT_APP_API_URL || "http://localhost:9000");

    socketServer.on("connect", () => {
      console.log("Connected to socket server");
    });

    socketServer.on("connect_error", (error) => {
      console.error("Connection failed:", error);
    });

    socketServer.on("disconnect", () => {
      console.log("Disconnected from socket server");
    });

    return () => {
      socketServer.disconnect();
    };
  }, []);

  useEffect(() => {
    if (!socket || !quill) return;

    const handleChange = (delta, oldData, source) => {
      if (source !== "user") return;
      socket.emit("send-changes", delta);
    };

    quill.on("text-change", handleChange);

    return () => {
      quill.off("text-change", handleChange);
    };
  }, [quill, socket]);

  useEffect(() => {
    if (!socket || !quill) return;

    const handleReceiveChange = (delta) => {
      quill.updateContents(delta);
    };

    socket.on("receive-changes", handleReceiveChange);

    return () => {
      socket.off("receive-changes", handleReceiveChange);
    };
  }, [quill, socket]);

  useEffect(() => {
    if (!socket || !quill) return;

    socket.once("load-document", (document) => {
      console.log("Document loaded from server:", document);
      quill.setContents(document);
      quill.enable();
    });

    console.log("Requesting document with ID:", id);
    socket.emit("get-document", id);
  }, [quill, socket, id]);

  useEffect(() => {
    if (!socket || !quill) return;

    const interval = setInterval(() => {
      console.log("Auto-saving document...");
      socket.emit("save-document", quill.getContents());
    }, 2000);

    return () => {
      clearInterval(interval);
    };
  }, [socket, quill]);

  return (
    <Component>
      <Box className="container" id="container" />
    </Component>
  );
};

export default Editor;