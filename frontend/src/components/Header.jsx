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
      className="sticky top-0 z-50 backdrop-blur-xl bg-dark-bg/80 border-b border-dark-border"
    >
      <nav className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-3 group">
            <motion.div
              whileHover={{ scale: 1.05 }}
              className="flex items-center space-x-2"
            >
              <div className="w-10 h-10 rounded-xl bg-gradient-fintech flex items-center justify-center shadow-glow">
                <span className="text-xl">💎</span>
              </div>
              <div>
                <div className="text-xl font-bold bg-gradient-to-r from-primary to-gradient-cyan bg-clip-text text-transparent">
                  Investe-AI
                </div>
                <div className="text-xs text-dark-muted -mt-1">
                  Powered by AI
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
                  className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 ${
                    item.highlight
                      ? 'bg-gradient-fintech text-white shadow-glow'
                      : isActive(item.path)
                      ? 'bg-dark-card text-primary border border-primary/30'
                      : 'text-dark-muted hover:text-dark-text hover:bg-dark-card'
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
            className="md:hidden p-2 rounded-lg hover:bg-dark-card transition-colors"
          >
            <svg
              className="w-6 h-6 text-dark-text"
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
            className="md:hidden py-4 border-t border-dark-border"
          >
            <div className="flex flex-col space-y-2">
              {navItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  onClick={() => setMobileMenuOpen(false)}
                >
                  <div
                    className={`px-4 py-3 rounded-lg font-medium transition-all ${
                      item.highlight
                        ? 'bg-gradient-fintech text-white'
                        : isActive(item.path)
                        ? 'bg-dark-card text-primary border border-primary/30'
                        : 'text-dark-muted hover:text-dark-text hover:bg-dark-card'
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
