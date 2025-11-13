import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import StockTicker from './components/StockTicker';
import Home from './pages/Home';
import Sobre from './pages/Sobre';
import Questionario from './pages/Questionario';
import Perfil from './pages/Perfil';
import Resultado from './pages/Resultado';
import Simulacao from './pages/Simulacao';

function App() {
  return (
    <Router>
      <div className="flex flex-col min-h-screen">
        <Header />
        <StockTicker />
        <main className="flex-grow">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/sobre" element={<Sobre />} />
            <Route path="/questionario" element={<Questionario />} />
            <Route path="/perfil" element={<Perfil />} />
            <Route path="/resultado" element={<Resultado />} />
            <Route path="/simulacao" element={<Simulacao />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
