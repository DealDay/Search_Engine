import './App.css';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Home from "./Pages/Home";

function App() {
  return (
    <Router>
      {/* <Navigation /> */}
      <main style={{'position':'relative', 'marginTop':'0%'}}>
        <Routes>
          <Route path="/" element={<Home/>} />
        </Routes>
      </main>
      {/* <Footer /> */}
    </Router>
  );
};

export default App;
