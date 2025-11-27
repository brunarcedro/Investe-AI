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
    <footer className="bg-white border-t-2 border-[#FFA3FF]/20 mt-auto">
      <div className="container mx-auto px-4 py-12">
        {/* Main Footer Content */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand Column */}
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-[#FFA3FF] to-[#FF6EC7] flex items-center justify-center shadow-lg text-white font-black">
                B
              </div>
              <div>
                <div className="text-lg font-black text-[#004543]">
                  Breno
                </div>
                <div className="text-xs text-gray-600">
                  IA de Investimentos
                </div>
              </div>
            </div>
            <p className="text-sm text-gray-600 leading-relaxed">
              Sistema Inteligente de Recomendação de Carteiras usando Redes Neurais Artificiais
            </p>
            {/* Tech Stack Badges */}
            <div className="flex flex-wrap gap-2">
              {techStack.map((tech) => (
                <div
                  key={tech.name}
                  className="px-2 py-1 bg-[#FFF5F8] rounded-full text-xs text-gray-600 flex items-center gap-1 border border-[#FFA3FF]/20"
                >
                  <span>{tech.icon}</span>
                  {tech.name}
                </div>
              ))}
            </div>
          </div>

          {/* Produto Column */}
          <div>
            <h4 className="font-bold text-[#004543] mb-4">Produto</h4>
            <ul className="space-y-2">
              {footerLinks.produto.map((link) => (
                <li key={link.name}>
                  <Link
                    to={link.path}
                    className="text-gray-600 hover:text-[#FFA3FF] transition-colors text-sm"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Tecnologia Column */}
          <div>
            <h4 className="font-bold text-[#004543] mb-4">Tecnologia</h4>
            <ul className="space-y-2">
              {footerLinks.tecnologia.map((link) => (
                <li key={link.name}>
                  <a
                    href={link.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-gray-600 hover:text-[#FFA3FF] transition-colors text-sm flex items-center gap-1"
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
            <h4 className="font-bold text-[#004543] mb-4">Contato</h4>
            <ul className="space-y-2">
              {footerLinks.contato.map((link) => (
                <li key={link.name}>
                  <a
                    href={link.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-gray-600 hover:text-[#FFA3FF] transition-colors text-sm flex items-center gap-1"
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
        <div className="border-t-2 border-[#FFA3FF]/10 my-8" />

        {/* Bottom Footer */}
        <div className="flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="text-sm text-gray-600 text-center md:text-left">
            <p>
              © {currentYear} <span className="text-[#FFA3FF] font-bold">Breno</span>.
              Desenvolvido por{' '}
              <a
                href="https://linkedin.com/in/brunarcedro"
                target="_blank"
                rel="noopener noreferrer"
                className="text-[#FFA3FF] hover:text-[#FF6EC7] transition-colors font-semibold"
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
            className="flex items-center gap-4 px-4 py-2 bg-[#FFF5F8] rounded-2xl border-2 border-[#FFA3FF]/20"
          >
            <div className="text-center">
              <div className="text-lg font-bold text-[#00DD70]">91%</div>
              <div className="text-xs text-gray-600">Acurácia</div>
            </div>
            <div className="h-8 w-px bg-[#FFA3FF]/20" />
            <div className="text-center">
              <div className="text-lg font-bold text-[#FFA3FF]">6</div>
              <div className="text-xs text-gray-600">Ativos</div>
            </div>
            <div className="h-8 w-px bg-[#FFA3FF]/20" />
            <div className="text-center">
              <div className="text-lg font-bold text-[#FFCC01]">1.2k</div>
              <div className="text-xs text-gray-600">Casos</div>
            </div>
          </motion.div>
        </div>

        {/* Disclaimer */}
        <div className="mt-8 pt-6 border-t-2 border-[#FFA3FF]/10">
          <p className="text-xs text-gray-600 text-center max-w-4xl mx-auto">
            <strong className="text-[#004543]">Aviso Legal:</strong> Este sistema foi desenvolvido para fins educacionais como Trabalho de Conclusão de Curso.
            As recomendações são baseadas em modelos de Inteligência Artificial e não constituem aconselhamento financeiro profissional.
            Sempre consulte um assessor de investimentos certificado antes de tomar decisões financeiras.
          </p>
        </div>
      </div>
    </footer>
  );
}
