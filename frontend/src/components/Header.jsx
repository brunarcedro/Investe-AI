import { Link } from 'react-router-dom';

export default function Header() {
  return (
    <header className="bg-white shadow-md">
      <nav className="container mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          <Link to="/" className="flex items-center space-x-2">
            <div className="text-2xl font-bold text-primary">
              💼 Investe-AI
            </div>
          </Link>

          <div className="hidden md:flex space-x-6">
            <Link to="/" className="text-gray-700 hover:text-primary transition">
              Início
            </Link>
            <Link to="/sobre" className="text-gray-700 hover:text-primary transition">
              Sobre
            </Link>
          </div>
        </div>
      </nav>
    </header>
  );
}
