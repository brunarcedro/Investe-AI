import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';

export default function Footer() {
  const currentYear = new Date().getFullYear();

  const footerLinks = {
    produto: [
      { name: 'Como Funciona', path: '/' },
      { name: 'Começar Análise', path: '/questionario' },
      { name: 'Sobre o Projeto', path: '/sobre' },
    ],
    tecnologia: [
      { name: 'Redes Neurais', external: true, url: 'https://github.com/brunarcedro/Investe-AI' },
      { name: 'GitHub', external: true, url: 'https://github.com/brunarcedro/Investe-AI' },
      { name: 'Documentação', external: true, url: 'https://github.com/brunarcedro/Investe-AI#readme' },
    ],
    contato: [
      { name: 'LinkedIn', external: true, url: 'https://linkedin.com/in/brunarcedro' },
      { name: 'GitHub', external: true, url: 'https://github.com/brunarcedro' },
      { name: 'Email', external: true, url: 'mailto:bruna@underlinetech.com.br' },
    ],
  };

  const techStack = [
    { name: 'React', icon: '⚛️' },
    { name: 'FastAPI', icon: '⚡' },
    { name: 'TensorFlow', icon: '🧠' },
    { name: 'Python', icon: '🐍' },
  ];

  return (
    <footer className="bg-dark-card border-t border-dark-border mt-auto">
      <div className="container mx-auto px-4 py-12">
        {/* Main Footer Content */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand Column */}
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <div className="w-10 h-10 rounded-xl bg-gradient-fintech flex items-center justify-center">
                <span className="text-xl">💎</span>
              </div>
              <div>
                <div className="text-lg font-bold bg-gradient-to-r from-primary to-gradient-cyan bg-clip-text text-transparent">
                  Investe-AI
                </div>
                <div className="text-xs text-dark-muted">
                  Powered by AI
                </div>
              </div>
            </div>
            <p className="text-sm text-dark-muted leading-relaxed">
              Sistema Inteligente de Recomendação de Carteiras usando Redes Neurais Artificiais
            </p>
            {/* Tech Stack Badges */}
            <div className="flex flex-wrap gap-2">
              {techStack.map((tech) => (
                <div
                  key={tech.name}
                  className="px-2 py-1 bg-dark-hover rounded text-xs text-dark-muted flex items-center gap-1"
                >
                  <span>{tech.icon}</span>
                  {tech.name}
                </div>
              ))}
            </div>
          </div>

          {/* Produto Column */}
          <div>
            <h4 className="font-bold text-dark-text mb-4">Produto</h4>
            <ul className="space-y-2">
              {footerLinks.produto.map((link) => (
                <li key={link.name}>
                  <Link
                    to={link.path}
                    className="text-dark-muted hover:text-primary transition-colors text-sm"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Tecnologia Column */}
          <div>
            <h4 className="font-bold text-dark-text mb-4">Tecnologia</h4>
            <ul className="space-y-2">
              {footerLinks.tecnologia.map((link) => (
                <li key={link.name}>
                  <a
                    href={link.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-dark-muted hover:text-primary transition-colors text-sm flex items-center gap-1"
                  >
                    {link.name}
                    <span className="text-xs">↗</span>
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Contato Column */}
          <div>
            <h4 className="font-bold text-dark-text mb-4">Contato</h4>
            <ul className="space-y-2">
              {footerLinks.contato.map((link) => (
                <li key={link.name}>
                  <a
                    href={link.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-dark-muted hover:text-primary transition-colors text-sm flex items-center gap-1"
                  >
                    {link.name}
                    <span className="text-xs">↗</span>
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Divider */}
        <div className="border-t border-dark-border my-8" />

        {/* Bottom Footer */}
        <div className="flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="text-sm text-dark-muted text-center md:text-left">
            <p>
              © {currentYear} <span className="text-primary font-semibold">Investe-AI</span>.
              Desenvolvido por{' '}
              <a
                href="https://linkedin.com/in/brunarcedro"
                target="_blank"
                rel="noopener noreferrer"
                className="text-primary hover:text-primary-light transition-colors"
              >
                Bruna Ribeiro Cedro
              </a>
            </p>
            <p className="text-xs mt-1">
              TCC - Sistemas de Informação | IFES
            </p>
          </div>

          {/* Stats Badge */}
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="flex items-center gap-4 px-4 py-2 bg-dark-hover rounded-lg"
          >
            <div className="text-center">
              <div className="text-lg font-bold text-success">91%</div>
              <div className="text-xs text-dark-muted">Acurácia</div>
            </div>
            <div className="h-8 w-px bg-dark-border" />
            <div className="text-center">
              <div className="text-lg font-bold text-primary">6</div>
              <div className="text-xs text-dark-muted">Ativos</div>
            </div>
            <div className="h-8 w-px bg-dark-border" />
            <div className="text-center">
              <div className="text-lg font-bold text-warning">1.2k</div>
              <div className="text-xs text-dark-muted">Casos</div>
            </div>
          </motion.div>
        </div>

        {/* Disclaimer */}
        <div className="mt-8 pt-6 border-t border-dark-border">
          <p className="text-xs text-dark-muted text-center max-w-4xl mx-auto">
            <strong>Aviso Legal:</strong> Este sistema foi desenvolvido para fins educacionais como Trabalho de Conclusão de Curso.
            As recomendações são baseadas em modelos de Inteligência Artificial e não constituem aconselhamento financeiro profissional.
            Sempre consulte um assessor de investimentos certificado antes de tomar decisões financeiras.
          </p>
        </div>
      </div>
    </footer>
  );
}
