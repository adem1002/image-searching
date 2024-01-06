/* eslint-disable no-unused-vars */
import Tab from "./Tab";
import "./style.css";
// eslint-disable-next-line react/prop-types
export default function Uploader({ setOpenUploader, setData, setImg }) {
  const handleModalClick = (e) => {
    // Stop the click event from propagating to the outer modal div
    e.stopPropagation();
  };
  return (
    <div
      className="modalOuter"
      onClick={() => {
        setOpenUploader(false);
      }}
    >
      <div className="modalBox" onClick={handleModalClick}>
        <h3 className="heading">Add your signature</h3>
        <p className="instruction">
          Upload an image or use signature-box to sign
        </p>
        <div className="Tabs">
          <Tab
            setOpenUploader={setOpenUploader}
            setData={setData}
            setImg={setImg}
          />
        </div>
      </div>
    </div>
  );
}
