/* eslint-disable react/prop-types */
/* eslint-disable no-unused-vars */
import { useEffect, useState } from "react";
import { FiUpload } from "react-icons/fi";

export default function Tab({ setOpenUploader, setData }) {
  const [file, setFile] = useState({
    selectedFile: null,
  });

  const [dragActive, setDragActive] = useState(false);
  const [msg, setMsg] = useState("");

  async function getImages() {
    const postData = new FormData();
    postData.append("file", file.selectedFile);

    const response = await fetch("http://127.0.0.1:5000/similar_images", {
      method: "POST",
      body: postData,
    });
    return response.json();
  }
  useEffect(() => {
    if (file.selectedFile != null) {
      getImages().then((res) => {
        setData(res);
        console.log(res);
      });
    }
  }, [file]);

  const checkFileType = (e, eventType) => {
    let extension;

    if (eventType === "drop") {
      extension = e.dataTransfer.files[0].name.match(/\.([^.]+)$/)[1];
    } else {
      extension = e.target.value.match(/\.([^.]+)$/)[1];
    }

    switch (extension) {
      case "jpg":
      case "jpeg":
      case "png":
      case "pdf":
        eventType !== "drop"
          ? setFile({ selectedFile: e.target.files[0] })
          : setFile({ selectedFile: e.dataTransfer.files[0] });
        setMsg("");
        break;
      default:
        setFile({ selectedFile: null });
        setMsg(`.${extension} format is not supported.`);
    }
  };

  const checkSize = (e, eventType) => {
    let size;
    if (eventType === "drop") {
      // console.log("size", e.dataTransfer.files[0]);
      size = e.dataTransfer.files[0].size / 8;
    } else {
      // console.log("size", e.target.files[0].size);
      size = e.target.files[0].size / 8;
    }
    // console.log("converted size", size);

    if (size <= 51200) {
      checkFileType(e, eventType);
    } else {
      setMsg("Size should be less than 50KB");
    }
  };

  const chooseFile = (e) => {
    if (e.target.files && e.target.files[0]) {
      checkSize(e);
      // checkFileType(e);
      // setOpenUploader(false);
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      checkSize(e, "drop");
      // setOpenUploader(false);
      // checkFileType(e, "drop");
    }
  };

  return (
    <div className="FirstTab">
      <form
        className="uploadBox"
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onSubmit={(e) => e.preventDefault()}
      >
        {file.selectedFile !== null ? (
          <p className="filename">{file.selectedFile.name}</p>
        ) : msg !== "" ? (
          msg
        ) : (
          <FiUpload className="upload-icon" />
        )}

        <div>
          <div className="drag">
            Drop your file here or{" "}
            <div className="browse">
              <label
                htmlFor="img"
                className="file-label"
                onClick={() => document.getElementById("getFile").click()}
              >
                Browse
                <input
                  type="file"
                  data-max-size="2048"
                  id="getFile"
                  className="fileIcon"
                  onChange={chooseFile}
                />
              </label>
            </div>
          </div>
        </div>

        <p className="info">Supported files: JPEG, PNG, PDF</p>
      </form>
    </div>
  );
}
