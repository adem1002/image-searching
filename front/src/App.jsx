import { useState } from "react";
import Images from "./components/Images";
import Modal from "./components/Modal";
import Navbar from "./components/navbar";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

function App() {
  const [selected, setSelected] = useState(null);
  const [text, setText] = useState("");
  const [clicked, setClicked] = useState(false);

  const queryClient = new QueryClient();

  return (
    <QueryClientProvider client={queryClient}>
      <div>
        <Navbar setClicked={setClicked} setText={setText} />
        <Images clicked={clicked} text={text} setSelected={setSelected} />
        <Modal selected={selected} setSelected={setSelected} />
      </div>
    </QueryClientProvider>
  );
}

export default App;
