import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import { healthCheck } from '../services/api';

export default function Home() {
  const [apiStatus, setApiStatus] = useState(null);

  useEffect(() => {
    checkAPI();
  }, []);

  const checkAPI = async () => {
    try {
      const data = await healthCheck();
      setApiStatus(data);
    } catch (error) {
      console.error('API offline:', error);
      setApiStatus({ status: 'offline' });
    }
  };

  const features = [
    {
      icon: '🧠',
      title: 'Inteligência Artificial',
      description: 'Duas redes neurais trabalhando juntas com 91% de acurácia na classificação de perfil',
      gradient: 'from-primary to-gradient-cyan',
    },
    {
      icon: '📊',
      title: 'Análise de Dados Reais',
      description: 'Simulações com cotações históricas do mercado brasileiro via Yahoo Finance',
      gradient: 'from-success to-gradient-cyan',
    },
    {
      icon: '🎯',
      title: 'Personalização Total',
      description: 'Carteira montada especificamente para seu perfil, objetivos e tolerância ao risco',
      gradient: 'from-warning to-gradient-pink',
    },
    {
      icon: '🔮',
      title: 'Projeções Futuras',
      description: 'Monte Carlo com 1000+ cenários probabilísticos para planejar seu futuro',
      gradient: 'from-gradient-purple to-gradient-pink',
    },
  ];

  const stats = [
    { label: 'Acurácia do Modelo', value: '91%', color: 'text-success' },
    { label: 'Classes de Ativos', value: '6', color: 'text-primary' },
    { label: 'Casos Analisados', value: '1.279', color: 'text-warning' },
    { label: 'R² Score', value: '>0.85', color: 'text-gradient-purple' },
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section com Glassmorphism */}
      <section className="relative overflow-hidden py-20 px-4">
        {/* Background Gradient Animation */}
        <div className="absolute inset-0 bg-gradient-to-br from-primary/20 via-gradient-purple/10 to-gradient-cyan/20 blur-3xl" />

        <div className="relative container mx-auto max-w-7xl">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center"
          >
            {/* Badge de Status */}
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.2 }}
              className="inline-flex items-center gap-2 px-4 py-2 bg-primary/10 border border-primary/30 rounded-full mb-6"
            >
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-success opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-success"></span>
              </span>
              <span className="text-sm font-medium text-dark-text">
                {apiStatus?.status === 'online' ? 'Sistema Operacional' : 'Verificando Sistema...'}
              </span>
            </motion.div>

            <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-primary via-gradient-purple to-gradient-cyan bg-clip-text text-transparent">
              Investe-AI
            </h1>

            <p className="text-xl md:text-2xl text-dark-text mb-4 max-w-3xl mx-auto">
              Sistema Inteligente de Recomendação de Carteiras de Investimento
            </p>

            <p className="text-lg text-dark-muted mb-12 max-w-2xl mx-auto">
              Tecnologia de <span className="text-primary font-semibold">Redes Neurais Artificiais</span> para
              democratizar o acesso a assessoria de investimentos personalizada
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/questionario">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="btn-premium text-lg px-10 py-4 w-full sm:w-auto"
                >
                  🚀 Começar Análise Gratuita
                </motion.button>
              </Link>

              <Link to="/sobre">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="bg-dark-card border-2 border-dark-border text-dark-text font-semibold px-10 py-4 rounded-xl hover:border-primary transition-all duration-300 w-full sm:w-auto"
                >
                  📚 Saiba Mais
                </motion.button>
              </Link>
            </div>
          </motion.div>

          {/* Stats Grid */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4, duration: 0.8 }}
            className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-20"
          >
            {stats.map((stat, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.5 + index * 0.1 }}
                className="glass-card p-6 text-center hover:scale-105 transition-transform duration-300 cursor-pointer"
              >
                <div className={`text-3xl md:text-4xl font-bold ${stat.color} mb-2`}>
                  {stat.value}
                </div>
                <div className="text-sm text-dark-muted">{stat.label}</div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 bg-dark-card/30">
        <div className="container mx-auto max-w-7xl">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              Por que escolher o <span className="text-primary">Investe-AI</span>?
            </h2>
            <p className="text-xl text-dark-muted max-w-2xl mx-auto">
              Tecnologia de ponta combinada com análise financeira especializada
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 gap-6">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ scale: 1.02 }}
                className="card-hover group cursor-pointer"
              >
                <div className={`text-5xl mb-4 transform group-hover:scale-110 transition-transform duration-300`}>
                  {feature.icon}
                </div>
                <h3 className="text-2xl font-bold mb-3 text-dark-text">
                  {feature.title}
                </h3>
                <p className="text-dark-muted leading-relaxed">
                  {feature.description}
                </p>
                <div className={`h-1 w-20 mt-4 rounded-full bg-gradient-to-r ${feature.gradient}`} />
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 px-4">
        <div className="container mx-auto max-w-7xl">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              Como <span className="text-primary">funciona</span>?
            </h2>
            <p className="text-xl text-dark-muted">
              4 passos simples para sua carteira personalizada
            </p>
          </motion.div>

          <div className="grid md:grid-cols-4 gap-6">
            {[
              { step: '01', title: 'Questionário', desc: 'Responda 10 perguntas sobre seu perfil financeiro', icon: '📝' },
              { step: '02', title: 'Análise IA', desc: 'Duas redes neurais analisam suas respostas', icon: '🧠' },
              { step: '03', title: 'Carteira', desc: 'Receba alocação personalizada em 6 classes de ativos', icon: '💼' },
              { step: '04', title: 'Simulação', desc: 'Veja projeções com dados reais do mercado', icon: '📈' },
            ].map((item, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.15 }}
                className="text-center"
              >
                <div className="relative inline-block mb-6">
                  <div className="text-6xl mb-2">{item.icon}</div>
                  <div className="absolute -top-2 -right-2 bg-gradient-fintech text-white text-xs font-bold px-2 py-1 rounded-full">
                    {item.step}
                  </div>
                </div>
                <h3 className="text-xl font-bold mb-2 text-dark-text">{item.title}</h3>
                <p className="text-dark-muted text-sm">{item.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Final */}
      <section className="py-20 px-4">
        <div className="container mx-auto max-w-4xl">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="glass-card p-12 text-center relative overflow-hidden"
          >
            {/* Gradient Background */}
            <div className="absolute inset-0 bg-gradient-to-br from-primary/10 via-gradient-purple/5 to-gradient-cyan/10" />

            <div className="relative z-10">
              <h2 className="text-4xl md:text-5xl font-bold mb-4">
                Pronto para começar?
              </h2>
              <p className="text-xl text-dark-muted mb-8 max-w-2xl mx-auto">
                Descubra seu perfil de investidor e receba uma carteira personalizada em menos de 3 minutos
              </p>

              <Link to="/questionario">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="btn-premium text-xl px-12 py-5"
                >
                  🎯 Iniciar Análise Agora
                </motion.button>
              </Link>

              <p className="text-sm text-dark-muted mt-6">
                ✓ Gratuito • ✓ Sem cadastro • ✓ Resultados instantâneos
              </p>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Disclaimer */}
      <section className="py-8 px-4 bg-dark-card/30 border-t border-dark-border">
        <div className="container mx-auto max-w-4xl text-center">
          <p className="text-sm text-dark-muted">
            <strong>Aviso Educacional:</strong> Este é um sistema desenvolvido para fins acadêmicos (TCC - Sistemas de Informação).
            As recomendações são baseadas em modelos de IA e não constituem aconselhamento financeiro profissional.
            Sempre consulte um assessor certificado antes de investir.
          </p>
        </div>
      </section>
    </div>
  );
}
