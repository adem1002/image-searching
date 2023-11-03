import { useState } from "react";
import Images from "./components/Images";
import Modal from "./components/Modal";
import Navbar from "./components/navbar";

function App() {
  const [selected, setSelected] = useState(null);
  console.log(selected);
  return (
    <div>
      <Navbar />
      <Images setSelected={setSelected} />
      <Modal selected={selected} setSelected={setSelected} />
    </div>
  );
}

export default App;
