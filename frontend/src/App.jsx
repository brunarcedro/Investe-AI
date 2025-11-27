import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Questionario from './pages/Questionario';
import Resultado from './pages/Resultado';
import Sobre from './pages/Sobre';

function App() {
  return (
    <Router>
      <div className="min-h-screen">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/questionario" element={<Questionario />} />
          <Route path="/resultado" element={<Resultado />} />
          <Route path="/sobre" element={<Sobre />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
