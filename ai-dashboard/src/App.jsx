import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Upload from "./pages/Upload";
import DatasetDetail from "./pages/DatasetDetail";
import Login from "./pages/Login";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/Dashboard" element={<Dashboard />} />
        <Route path="/upload" element={<Upload />} />
        <Route path="/dataset/:id" element={<DatasetDetail />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;