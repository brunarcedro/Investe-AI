import { Link, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useState } from 'react';

export default function Header() {
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navItems = [
    { name: 'Início', path: '/', icon: '🏠' },
    { name: 'Sobre', path: '/sobre', icon: '📚' },
    { name: 'Começar', path: '/questionario', icon: '🚀', highlight: true },
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <motion.header
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className="sticky top-0 z-50 backdrop-blur-xl bg-white/90 border-b-2 border-[#FFA3FF]/20 shadow-sm"
    >
      <nav className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          {/* Logo Breno */}
          <Link to="/" className="flex items-center space-x-3 group">
            <motion.div
              whileHover={{ scale: 1.05 }}
              className="flex items-center space-x-2"
            >
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-[#FFA3FF] to-[#FF6EC7] flex items-center justify-center shadow-lg text-white font-black">
                B
              </div>
              <div>
                <div className="text-xl font-black text-[#004543]">
                  Breno
                </div>
                <div className="text-xs text-gray-600 -mt-1">
                  IA de Investimentos
                </div>
              </div>
            </motion.div>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-2">
            {navItems.map((item) => (
              <Link key={item.path} to={item.path}>
                <motion.div
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className={`px-4 py-2 rounded-full font-bold transition-all duration-300 ${
                    item.highlight
                      ? 'bg-gradient-to-r from-[#FFA3FF] to-[#FF6EC7] text-white shadow-md'
                      : isActive(item.path)
                      ? 'bg-[#FFF5F8] text-[#FFA3FF] border-2 border-[#FFA3FF]'
                      : 'text-gray-600 hover:text-[#004543] hover:bg-[#FFF5F8]'
                  }`}
                >
                  <span className="mr-2">{item.icon}</span>
                  {item.name}
                </motion.div>
              </Link>
            ))}
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 rounded-lg hover:bg-[#FFF5F8] transition-colors"
          >
            <svg
              className="w-6 h-6 text-[#004543]"
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              {mobileMenuOpen ? (
                <path d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="md:hidden py-4 border-t-2 border-[#FFA3FF]/20"
          >
            <div className="flex flex-col space-y-2">
              {navItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  onClick={() => setMobileMenuOpen(false)}
                >
                  <div
                    className={`px-4 py-3 rounded-full font-bold transition-all ${
                      item.highlight
                        ? 'bg-gradient-to-r from-[#FFA3FF] to-[#FF6EC7] text-white'
                        : isActive(item.path)
                        ? 'bg-[#FFF5F8] text-[#FFA3FF] border-2 border-[#FFA3FF]'
                        : 'text-gray-600 hover:text-[#004543] hover:bg-[#FFF5F8]'
                    }`}
                  >
                    <span className="mr-2">{item.icon}</span>
                    {item.name}
                  </div>
                </Link>
              ))}
            </div>
          </motion.div>
        )}
      </nav>
    </motion.header>
  );
}
