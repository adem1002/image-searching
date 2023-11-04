import { useState } from "react";
import Images from "./components/Images";
import Modal from "./components/Modal";
import Navbar from "./components/navbar";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

function App() {
  const [selected, setSelected] = useState(null);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const queryClient = new QueryClient();

  return (
    <QueryClientProvider client={queryClient}>
      <div>
        <Navbar setData={setData} setLoading={setLoading} />
        <Images data={data} setSelected={setSelected} loading={loading} />
        <Modal selected={selected} setSelected={setSelected} />
      </div>
    </QueryClientProvider>
  );
}

export default App;
