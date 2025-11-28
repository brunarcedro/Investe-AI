import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-academic-bg">
      {/* Header */}
      <header className="border-b border-academic-border bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-primary">Investe-AI</h1>
              <p className="text-sm text-academic-text-muted">Sistema Inteligente de Recomendação de Investimentos</p>
            </div>
            <nav className="hidden md:flex gap-6">
              <button onClick={() => navigate('/')} className="text-academic-text-secondary hover:text-primary transition-colors font-medium">
                Início
              </button>
              <button onClick={() => navigate('/sobre')} className="text-academic-text-secondary hover:text-primary transition-colors font-medium">
                Sobre
              </button>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-24">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <div className="inline-block mb-6 px-4 py-2 bg-primary-50 rounded-full">
              <span className="text-primary font-semibold text-sm">Trabalho de Conclusão de Curso • IFES</span>
            </div>

            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-academic-text mb-6 leading-tight">
              Análise de Perfil de Investidor com{' '}
              <span className="text-primary">Inteligência Artificial</span>
            </h1>

            <p className="text-lg md:text-xl text-academic-text-secondary mb-12 leading-relaxed max-w-3xl mx-auto">
              Sistema baseado em <strong>Dual Ensemble Architecture</strong> com Voting Classifier e Ensemble V4
              para classificação de perfil de risco (88,2%) e alocação personalizada (R²=82%).
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button
                onClick={() => navigate('/questionario')}
                className="btn-primary text-lg px-8 py-4"
              >
                Iniciar Análise Completa
              </button>
              <button
                onClick={() => navigate('/sobre')}
                className="btn-secondary text-lg px-8 py-4"
              >
                Saiba Mais
              </button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 bg-academic-bg-secondary">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="text-center mb-12"
          >
            <h2 className="section-title">Arquitetura do Sistema</h2>
            <p className="text-academic-text-secondary">
              Tecnologias e metodologias aplicadas no desenvolvimento
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="card-academic p-8"
            >
              <div className="w-12 h-12 bg-primary-50 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h3 className="subsection-title">Voting Classifier</h3>
              <p className="text-academic-text-secondary text-sm leading-relaxed">
                Ensemble com RF + MLP(15,10,5) + SVM com soft voting ponderado
                alcançando <strong className="text-primary">88,2% de acurácia</strong>.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="card-academic p-8"
            >
              <div className="w-12 h-12 bg-primary-50 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="subsection-title">Arquitetura Dual</h3>
              <p className="text-academic-text-secondary text-sm leading-relaxed">
                Duas redes neurais especializadas: classificação de perfil de risco e
                alocação de portfólio com <strong className="text-primary">R²=0,85</strong>.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: 0.3 }}
              className="card-academic p-8"
            >
              <div className="w-12 h-12 bg-primary-50 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
                </svg>
              </div>
              <h3 className="subsection-title">Dataset Híbrido</h3>
              <p className="text-academic-text-secondary text-sm leading-relaxed">
                1.279 registros combinando dados do <strong className="text-primary">SCF (76%)</strong> e
                dados sintéticos brasileiros (24%), validados por especialista.
              </p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Metrics Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="text-center mb-12"
          >
            <h2 className="section-title">Métricas de Performance</h2>
            <p className="text-academic-text-secondary">
              Resultados obtidos com validação cruzada 5-fold estratificada
            </p>
          </motion.div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div className="text-center p-6 bg-white border border-academic-border rounded-lg">
              <div className="text-4xl font-bold text-primary mb-2">91,5%</div>
              <div className="text-sm font-medium text-academic-text">Acurácia</div>
              <div className="text-xs text-academic-text-muted mt-1">IC 95%: [91,0%, 92,0%]</div>
            </div>

            <div className="text-center p-6 bg-white border border-academic-border rounded-lg">
              <div className="text-4xl font-bold text-primary mb-2">73ms</div>
              <div className="text-sm font-medium text-academic-text">Latência</div>
              <div className="text-xs text-academic-text-muted mt-1">Tempo médio</div>
            </div>

            <div className="text-center p-6 bg-white border border-academic-border rounded-lg">
              <div className="text-4xl font-bold text-primary mb-2">0,85</div>
              <div className="text-sm font-medium text-academic-text">R² Score</div>
              <div className="text-xs text-academic-text-muted mt-1">Alocação</div>
            </div>

            <div className="text-center p-6 bg-white border border-academic-border rounded-lg">
              <div className="text-4xl font-bold text-primary mb-2">2,78%</div>
              <div className="text-sm font-medium text-academic-text">MAE</div>
              <div className="text-xs text-academic-text-muted mt-1">Erro médio</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 bg-academic-bg-secondary">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-3xl md:text-4xl font-bold text-academic-text mb-6">
              Descubra Seu Perfil de Investidor
            </h2>
            <p className="text-lg text-academic-text-secondary mb-8">
              Análise completa em menos de 2 minutos com recomendações personalizadas
              geradas por inteligência artificial.
            </p>
            <button
              onClick={() => navigate('/questionario')}
              className="btn-primary text-lg px-12 py-4"
            >
              Começar Análise Gratuita
            </button>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-academic-border bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <p className="text-sm text-academic-text-secondary mb-2">
              <strong>Trabalho de Conclusão de Curso</strong> • Sistemas de Informação • IFES
            </p>
            <p className="text-xs text-academic-text-muted">
              Desenvolvido por Bruna Ribeiro Cedro • 2025
            </p>
            <p className="text-xs text-academic-text-muted mt-4">
              Sistema desenvolvido para fins acadêmicos. As recomendações não constituem aconselhamento financeiro profissional.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
