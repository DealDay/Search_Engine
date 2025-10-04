import './App.css';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Home from "./Pages/Home";
import ResultPage from './Pages/ResultPage';

function App() {
  return (
    <Router>
      {/* <Navigation /> */}
      <main style={{'position':'relative', 'marginTop':'0%'}}>
        <Routes>
          <Route path="/" caseSensitive={false} element={<Home/>} />
          <Route
            path="/:searchWord"
            caseSensitive={false}
            element={<ResultPage />}
          />
        </Routes>
      </main>
      {/* <Footer /> */}
    </Router>
  );
};

export default App;
