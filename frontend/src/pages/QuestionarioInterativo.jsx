import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { recomendarPortfolio } from '../services/api';
import ChatMessage from '../components/ChatMessage';
import UserMessageButton from '../components/UserMessageButton';
import ProfileCharacter from '../components/ProfileCharacter';
import confetti from 'canvas-confetti';

export default function QuestionarioInterativo() {
  const navigate = useNavigate();
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [showQuestion, setShowQuestion] = useState(false);
  const [loading, setLoading] = useState(false);
  const [showResult, setShowResult] = useState(false);
  const [profileResult, setProfileResult] = useState(null);
  const [currentCardIndex, setCurrentCardIndex] = useState(0);
  const [selectedResponse, setSelectedResponse] = useState(null);
  const [showBrenoResponse, setShowBrenoResponse] = useState(false);

  const [answers, setAnswers] = useState({
    idade: 25,
    toleranciaRisco: 5,
    objetivos: [],
    reacaoPerda: '',
    horizonte: '',
    rendaMensal: '',
    patrimonioAtual: 0,
    reservaEmergencia: false,
    experiencia: 0,
  });

  const questions = [
    {
      type: 'intro',
      messages: [
        'Fala! 👋 Eu sou o Breno, seu parceiro de investimentos!',
        'Antes de você sair investindo por aí, preciso te contar um segredo...',
        '🎯 Conhecer seu PERFIL DE INVESTIDOR é tipo descobrir seu superpoder financeiro!',
        'É ele que vai te mostrar quais investimentos combinam com você, quanto risco você aguenta, e como montar uma carteira que te deixa tranquilo(a) dormindo de noite! 😴💰',
        'Investir sem conhecer seu perfil é tipo jogar videogame no escuro... pode até dar certo, mas as chances de bater a cara são grandes! 😅',
        'Então bora descobrir qual é o SEU estilo? Prometo que vai ser divertido! 🚀'
      ]
    },
    {
      type: 'message-buttons',
      question: 'Primeiro, me conta: você já investe ou tá começando agora?',
      key: 'experiencia',
      options: [
        { value: 0, label: 'Tô começando agora! 🌱', response: 'Que massa! Todo mundo começa de algum lugar. Vou te guiar com calma!' },
        { value: 2, label: 'Já invisto há um tempo! 💪', response: 'Showw! Já tem experiência, isso vai ajudar muito!' }
      ]
    },
    {
      type: 'age-chat',
      question: 'Você sabia que a idade é um fator SUPER importante pro seu perfil? 🎂',
      explanation: 'Quanto mais novo você é, mais tempo tem pra investir e se recuperar de oscilações. Já quem tá mais perto da aposentadoria geralmente prefere mais segurança!',
      followUp: 'Então me diz, quantos anos você tem?',
      key: 'idade',
      min: 18,
      max: 100
    },
    {
      type: 'slider',
      question: 'Agora a pergunta de MILHÕES! 💎 Quando o mercado fica louco e seus investimentos caem 15% em um mês, qual é sua vibe?',
      key: 'toleranciaRisco',
      options: [
        { value: 1, label: 'SOS! 😰', sublabel: 'Já tiro tudo fora', emoji: '🐢', color: '#00DD70' },
        { value: 5, label: 'Calma... 🧘', sublabel: 'Respiro fundo e espero', emoji: '⚖️', color: '#FFCC01' },
        { value: 10, label: 'AEEE! 🤑', sublabel: 'Hora de comprar mais barato!', emoji: '🚀', color: '#FFA3FF' }
      ]
    },
    {
      type: 'carousel-cards',
      question: 'Agora me conta, qual é o seu MAIOR sonho financeiro? 🌟 (Desliza pros lados pra ver as opções!)',
      key: 'objetivos',
      multiple: false,
      options: [
        { id: 'aumentar', label: 'Ver meu dinheiro crescer', icon: '💰', description: 'Quero multiplicar meu patrimônio!', gradient: 'from-[#00DD70] to-[#B5FECC]' },
        { id: 'imovel', label: 'Comprar meu cantinho', icon: '🏡', description: 'Sonho com minha casa própria!', gradient: 'from-[#FFCC01] to-[#FFEE88]' },
        { id: 'futuro', label: 'Investir no meu futuro', icon: '🎓', description: 'Educação, viagens, experiências!', gradient: 'from-[#FFA3FF] to-[#FFEE88]' },
        { id: 'aposentadoria', label: 'Aposentadoria dos sonhos', icon: '🌴', description: 'Quero viver de renda no futuro!', gradient: 'from-[#004543] to-[#00DD70]' },
        { id: 'aprender', label: 'Aprender a investir', icon: '💡', description: 'Quero entender esse mundo!', gradient: 'from-[#FFCC01] to-[#FFA3FF]' }
      ]
    },
    {
      type: 'horizon',
      question: 'Por quanto tempo você pretende deixar essa grana investida? ⏰',
      key: 'horizonte',
      options: [
        { id: 'curto', label: 'Até 1 ano', desc: 'Preciso usar logo!', icon: '📅', color: '#FFCC01' },
        { id: 'medio', label: '1 a 5 anos', desc: 'Tenho um plano médio prazo', icon: '📆', color: '#00DD70' },
        { id: 'longo', label: 'Mais de 5 anos', desc: 'Penso no futuro distante', icon: '🗓️', color: '#004543' }
      ]
    },
    {
      type: 'income',
      question: 'Qual é a sua renda mensal? (Relaxa, isso fica entre nós! 🤐)',
      key: 'rendaMensal',
      options: [
        { id: 'ate2k', label: 'Até R$ 2.000', value: 2000, emoji: '🌱' },
        { id: '2k-5k', label: 'R$ 2.000 - R$ 5.000', value: 3500, emoji: '🌿' },
        { id: '5k-10k', label: 'R$ 5.000 - R$ 10.000', value: 7500, emoji: '🌳' },
        { id: 'acima10k', label: 'Acima de R$ 10.000', value: 15000, emoji: '🌲' }
      ]
    },
    {
      type: 'boolean',
      question: 'Última pergunta! Você tem uma reserva de emergência guardada? 🆘💰',
      explanation: '(Tipo uns 6 meses de despesas num lugar seguro e fácil de sacar)',
      key: 'reservaEmergencia'
    }
  ];

  useEffect(() => {
    if (currentQuestion === 0) {
      // Mostra mensagens de intro sequencialmente
      const timer = setTimeout(() => {
        setShowQuestion(true);
      }, questions[0].messages.length * 2000);
      return () => clearTimeout(timer);
    } else {
      const timer = setTimeout(() => {
        setShowQuestion(true);
      }, 800);
      return () => clearTimeout(timer);
    }
  }, [currentQuestion]);

  const handleAnswer = (value) => {
    const question = questions[currentQuestion];

    if (question.type === 'cards' && question.multiple) {
      const current = answers[question.key] || [];
      const updated = current.includes(value)
        ? current.filter(v => v !== value)
        : [...current, value];
      setAnswers({ ...answers, [question.key]: updated });
    } else {
      setAnswers({ ...answers, [question.key]: value });

      // Confete ao responder
      if (question.type === 'number') {
        confetti({
          particleCount: 50,
          spread: 60,
          origin: { y: 0.6 }
        });
      }
    }
  };

  const handleNext = () => {
    setShowQuestion(false);

    if (currentQuestion < questions.length - 1) {
      setTimeout(() => {
        setCurrentQuestion(currentQuestion + 1);
      }, 300);
    } else {
      handleSubmit();
    }
  };

  const handleSubmit = async () => {
    setLoading(true);

    try {
      // Mapear respostas para formato da API v2
      const apiData = {
        idade: answers.idade,
        renda_mensal: answers.rendaMensal || 0,
        patrimonio_total: answers.patrimonioAtual || 0,
        experiencia_investimento: answers.experiencia || 0,
        objetivo_principal: answers.objetivos.length > 0 ? answers.objetivos[0] : 'aumentar',
        horizonte_investimento: answers.horizonte === 'curto' ? 1 : answers.horizonte === 'medio' ? 3 : 10,
        tolerancia_risco: answers.toleranciaRisco <= 3 ? 'baixa' : answers.toleranciaRisco <= 7 ? 'media' : 'alta',
        conhecimento_mercado: answers.experiencia > 2 ? 'avancado' : answers.experiencia > 0 ? 'intermediario' : 'iniciante',
        tem_reserva_emergencia: answers.reservaEmergencia || false,
        percentual_investir: 10.0
      };

      // IMPORTANTE: Usar recomendarPortfolio que conecta Rede 1 → Rede 2
      const result = await recomendarPortfolio(apiData);

      // Salvar resultado no localStorage
      localStorage.setItem('resultado_investimento', JSON.stringify(result));

      // Salvar resultado COMPLETO da API
      setProfileResult(result);
      setShowResult(true);

      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 }
      });
    } catch (error) {
      console.error('Erro ao classificar perfil:', error);
      alert('Ops! Algo deu errado. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  const handleContinue = () => {
    // Navegar para resultado (dados já estão no localStorage)
    navigate('/resultado');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-academic-bg">
        <div className="text-center card-academic p-12 max-w-md">
          <motion.div
            animate={{ rotate: 360, scale: [1, 1.2, 1] }}
            transition={{ duration: 2, repeat: Infinity }}
            className="text-8xl mb-6"
          >
            🧠
          </motion.div>
          <h2 className="text-3xl font-bold text-academic-text mb-4">Analisando seu perfil...</h2>
          <p className="text-lg text-academic-text-secondary mb-6">Processando com Inteligência Artificial</p>
          <div className="flex justify-center gap-3">
            <motion.div
              animate={{ y: [0, -20, 0] }}
              transition={{ duration: 0.6, repeat: Infinity, delay: 0 }}
              className="w-4 h-4 bg-primary rounded-full"
            />
            <motion.div
              animate={{ y: [0, -20, 0] }}
              transition={{ duration: 0.6, repeat: Infinity, delay: 0.1 }}
              className="w-4 h-4 bg-primary-light rounded-full"
            />
            <motion.div
              animate={{ y: [0, -20, 0] }}
              transition={{ duration: 0.6, repeat: Infinity, delay: 0.2 }}
              className="w-4 h-4 bg-accent rounded-full"
            />
          </div>
        </div>
      </div>
    );
  }

  if (showResult && profileResult) {
    return <ProfileCharacter profile={profileResult} onContinue={handleContinue} />;
  }

  const currentQ = questions[currentQuestion];

  return (
    <div className="min-h-screen py-8 px-4 bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <div className="container mx-auto max-w-3xl">
        {/* Progress bar */}
        <div className="mb-6 bg-white rounded-2xl p-4 shadow-md border-2 border-blue-100">
          <div className="flex justify-between text-sm font-bold text-slate-800 mb-3">
            <span>Pergunta {currentQuestion + 1} de {questions.length}</span>
            <span className="text-blue-600">{Math.round(((currentQuestion + 1) / questions.length) * 100)}%</span>
          </div>
          <div className="h-3 bg-gray-100 rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-gradient-to-r from-blue-500 to-indigo-600"
              initial={{ width: 0 }}
              animate={{ width: `${((currentQuestion + 1) / questions.length) * 100}%` }}
              transition={{ duration: 0.5 }}
            />
          </div>
        </div>

        {/* Chat container */}
        <div className="space-y-6">
          {/* Intro messages */}
          {currentQ.type === 'intro' && (
            <>
              {currentQ.messages.map((msg, idx) => (
                <ChatMessage
                  key={idx}
                  message={msg}
                  isTyping={true}
                  delay={idx * 2000}
                />
              ))}
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: currentQ.messages.length * 2 }}
                className="text-center mt-8"
              >
                <button
                  onClick={handleNext}
                  className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-lg px-12 py-5 rounded-full font-bold shadow-2xl hover:scale-110 transition-transform"
                >
                  Bora descobrir meu perfil! 🚀
                </button>
              </motion.div>
            </>
          )}

          {/* Message Buttons - Estilo conversa com botões de resposta */}
          {currentQ.type === 'message-buttons' && (
            <>
              <ChatMessage message={currentQ.question} isTyping={true} delay={0} />

              {showQuestion && (
                <>
                  <div className="space-y-3 mt-6">
                    {currentQ.options.map((opt) => (
                      <UserMessageButton
                        key={opt.value}
                        text={opt.label}
                        onClick={() => {
                          setSelectedResponse(opt);
                          setAnswers({ ...answers, [currentQ.key]: opt.value });
                          setShowBrenoResponse(true);
                          confetti({
                            particleCount: 30,
                            spread: 40,
                            origin: { y: 0.7 }
                          });
                        }}
                        selected={selectedResponse?.value === opt.value}
                      />
                    ))}
                  </div>

                  {showBrenoResponse && selectedResponse && (
                    <>
                      <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.3 }}
                      >
                        <ChatMessage message={selectedResponse.response} isTyping={true} delay={300} />
                      </motion.div>

                      <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 1.5 }}
                        className="text-center mt-6"
                      >
                        <button
                          onClick={() => {
                            setSelectedResponse(null);
                            setShowBrenoResponse(false);
                            handleNext();
                          }}
                          className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-8 py-3 rounded-full font-bold shadow-lg hover:scale-105 transition-transform"
                        >
                          Próxima! 🚀
                        </button>
                      </motion.div>
                    </>
                  )}
                </>
              )}
            </>
          )}

          {/* Age Chat - Pergunta sobre idade com contexto educacional */}
          {currentQ.type === 'age-chat' && (
            <>
              <ChatMessage message={currentQ.question} isTyping={true} delay={0} />

              {showQuestion && (
                <>
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.8 }}
                  >
                    <ChatMessage message={currentQ.explanation} isTyping={true} delay={800} />
                  </motion.div>

                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 1.8 }}
                  >
                    <ChatMessage message={currentQ.followUp} isTyping={true} delay={1800} />
                  </motion.div>

                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 2.5 }}
                    className="mt-6"
                  >
                    <div className="bg-gradient-to-br from-[#004543]/20 to-[#B5FECC]/30 border-2 border-[#00DD70] rounded-3xl p-8 backdrop-blur-sm">
                      <div className="flex items-center justify-center gap-6">
                        <button
                          onClick={() => handleAnswer(Math.max(currentQ.min, answers[currentQ.key] - 1))}
                          className="w-14 h-14 rounded-full bg-gradient-to-br from-[#FFCC01] to-[#FFEE88] text-[#004543] flex items-center justify-center text-3xl font-bold hover:scale-110 transition-transform shadow-lg"
                        >
                          -
                        </button>
                        <div className="text-center">
                          <input
                            type="number"
                            value={answers[currentQ.key]}
                            onChange={(e) => handleAnswer(parseInt(e.target.value) || currentQ.min)}
                            min={currentQ.min}
                            max={currentQ.max}
                            className="w-24 text-center text-6xl font-bold bg-transparent border-none outline-none text-[#004543]"
                          />
                          <p className="text-sm text-gray-700 mt-2 font-bold">anos</p>
                        </div>
                        <button
                          onClick={() => handleAnswer(Math.min(currentQ.max, answers[currentQ.key] + 1))}
                          className="w-14 h-14 rounded-full bg-gradient-to-br from-[#FFCC01] to-[#FFEE88] text-[#004543] flex items-center justify-center text-3xl font-bold hover:scale-110 transition-transform shadow-lg"
                        >
                          +
                        </button>
                      </div>
                    </div>

                    <div className="text-center mt-6">
                      <button
                        onClick={handleNext}
                        className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-10 py-4 rounded-full font-bold shadow-lg hover:scale-105 transition-transform"
                      >
                        Confirmar idade! ✅
                      </button>
                    </div>
                  </motion.div>
                </>
              )}
            </>
          )}

          {/* Carousel Cards - Cards deslizáveis */}
          {currentQ.type === 'carousel-cards' && (
            <>
              <ChatMessage message={currentQ.question} isTyping={true} delay={0} />

              {showQuestion && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.8 }}
                  className="mt-6"
                >
                  <div className="relative max-w-md mx-auto">
                    <AnimatePresence mode="wait">
                      {currentQ.options.map((opt, idx) => {
                        if (idx !== currentCardIndex) return null;

                        const isSelected = answers[currentQ.key] === opt.id;

                        return (
                          <motion.div
                            key={opt.id}
                            initial={{ opacity: 0, x: 100 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -100 }}
                            className={`p-8 rounded-3xl cursor-pointer transition-all ${
                              isSelected ? 'ring-4 ring-[#FFCC01]' : ''
                            }`}
                            style={{
                              background: `linear-gradient(135deg, ${opt.gradient.replace('from-', '').replace('to-', ', ')})`,
                            }}
                            onClick={() => {
                              setAnswers({ ...answers, [currentQ.key]: opt.id });
                              confetti({
                                particleCount: 50,
                                spread: 60,
                                origin: { y: 0.6 }
                              });
                            }}
                          >
                            <div className="text-center">
                              <div className="text-7xl mb-4">{opt.icon}</div>
                              <h3 className="text-2xl font-bold text-[#004543] mb-2">{opt.label}</h3>
                              <p className="text-gray-700 font-medium">{opt.description}</p>
                            </div>
                          </motion.div>
                        );
                      })}
                    </AnimatePresence>

                    {/* Navegação do carousel */}
                    <div className="flex justify-between items-center mt-6">
                      <button
                        onClick={() => setCurrentCardIndex(Math.max(0, currentCardIndex - 1))}
                        disabled={currentCardIndex === 0}
                        className="px-6 py-3 rounded-full bg-[#004543] text-white font-bold disabled:opacity-30 hover:scale-105 transition-transform"
                      >
                        ← Anterior
                      </button>

                      <div className="flex gap-2">
                        {currentQ.options.map((_, idx) => (
                          <div
                            key={idx}
                            className={`w-2 h-2 rounded-full transition-all ${
                              idx === currentCardIndex ? 'bg-[#FFCC01] w-6' : 'bg-[#004543]/30'
                            }`}
                          />
                        ))}
                      </div>

                      <button
                        onClick={() => setCurrentCardIndex(Math.min(currentQ.options.length - 1, currentCardIndex + 1))}
                        disabled={currentCardIndex === currentQ.options.length - 1}
                        className="px-6 py-3 rounded-full bg-[#004543] text-white font-bold disabled:opacity-30 hover:scale-105 transition-transform"
                      >
                        Próximo →
                      </button>
                    </div>

                    {/* Botão de confirmar */}
                    {answers[currentQ.key] && (
                      <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="text-center mt-6"
                      >
                        <button
                          onClick={() => {
                            setCurrentCardIndex(0);
                            handleNext();
                          }}
                          className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-10 py-4 rounded-full font-bold shadow-lg hover:scale-105 transition-transform"
                        >
                          Escolho esse! 🎯
                        </button>
                      </motion.div>
                    )}
                  </div>
                </motion.div>
              )}
            </>
          )}

          {/* Regular questions */}
          {currentQ.type !== 'intro' && currentQ.type !== 'message-buttons' && currentQ.type !== 'age-chat' && currentQ.type !== 'carousel-cards' && (
            <>
              <ChatMessage message={currentQ.question} isTyping={false} />

              <AnimatePresence mode="wait">
                {showQuestion && (
                  <motion.div
                    key={currentQuestion}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    className="ml-14"
                  >
                    {/* Number input */}
                    {currentQ.type === 'number' && (
                      <div className="glass-card p-6">
                        <div className="flex items-center justify-center gap-4">
                          <button
                            onClick={() => handleAnswer(Math.max(currentQ.min, answers[currentQ.key] - 1))}
                            className="w-12 h-12 rounded-full bg-dark-hover border border-dark-border flex items-center justify-center text-2xl hover:bg-primary hover:border-primary transition-all"
                          >
                            -
                          </button>
                          <input
                            type="number"
                            value={answers[currentQ.key]}
                            onChange={(e) => handleAnswer(parseInt(e.target.value) || currentQ.min)}
                            min={currentQ.min}
                            max={currentQ.max}
                            className="w-32 text-center text-4xl font-bold bg-transparent border-none outline-none text-dark-text"
                          />
                          <button
                            onClick={() => handleAnswer(Math.min(currentQ.max, answers[currentQ.key] + 1))}
                            className="w-12 h-12 rounded-full bg-dark-hover border border-dark-border flex items-center justify-center text-2xl hover:bg-primary hover:border-primary transition-all"
                          >
                            +
                          </button>
                        </div>
                      </div>
                    )}

                    {/* Slider */}
                    {currentQ.type === 'slider' && (
                      <div className="bg-gradient-to-br from-white/80 to-[#B5FECC]/20 backdrop-blur-md border-2 border-[#00DD70]/30 rounded-3xl p-8 shadow-xl">
                        <input
                          type="range"
                          min="1"
                          max="10"
                          value={answers[currentQ.key]}
                          onChange={(e) => handleAnswer(parseInt(e.target.value))}
                          className="w-full h-4 bg-gradient-to-r from-[#00DD70]/30 to-[#FFA3FF]/30 rounded-full appearance-none cursor-pointer"
                          style={{
                            background: `linear-gradient(to right, #00DD70 0%, #FFCC01 50%, #FFA3FF 100%)`
                          }}
                        />
                        <div className="flex justify-between mt-8">
                          {currentQ.options.map((opt) => (
                            <div
                              key={opt.value}
                              className={`text-center transition-all ${
                                answers[currentQ.key] >= opt.value - 2 && answers[currentQ.key] <= opt.value + 2
                                  ? 'opacity-100 scale-125'
                                  : 'opacity-30 scale-90'
                              }`}
                            >
                              <div className="text-5xl mb-3">{opt.emoji}</div>
                              <div className="font-bold text-[#004543] text-base">{opt.label}</div>
                              <div className="text-sm text-gray-600 font-bold">{opt.sublabel}</div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Cards */}
                    {currentQ.type === 'cards' && (
                      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                        {currentQ.options.map((opt) => {
                          const isSelected = currentQ.multiple
                            ? (answers[currentQ.key] || []).includes(opt.id)
                            : answers[currentQ.key] === opt.id;

                          return (
                            <motion.button
                              key={opt.id}
                              onClick={() => handleAnswer(opt.id)}
                              whileHover={{ scale: 1.05 }}
                              whileTap={{ scale: 0.95 }}
                              className={`glass-card p-6 text-center transition-all ${
                                isSelected ? 'ring-2 ring-primary bg-primary/10' : ''
                              }`}
                            >
                              <div className="text-4xl mb-3">{opt.icon}</div>
                              <div className="text-sm font-semibold text-dark-text">{opt.label}</div>
                            </motion.button>
                          );
                        })}
                      </div>
                    )}

                    {/* Choice buttons */}
                    {currentQ.type === 'choice' && (
                      <div className="space-y-3">
                        {currentQ.options.map((opt) => (
                          <motion.button
                            key={opt.id}
                            onClick={() => handleAnswer(opt.id)}
                            whileHover={{ scale: 1.02 }}
                            whileTap={{ scale: 0.98 }}
                            className={`w-full glass-card p-4 flex items-center gap-4 text-left transition-all ${
                              answers[currentQ.key] === opt.id ? 'ring-2 ring-primary bg-primary/10' : ''
                            }`}
                          >
                            <div className="text-3xl">{opt.emoji}</div>
                            <div className="flex-1 text-dark-text">{opt.label}</div>
                          </motion.button>
                        ))}
                      </div>
                    )}

                    {/* Horizon, Income, Experience - similar pattern */}
                    {(currentQ.type === 'horizon' || currentQ.type === 'income' || currentQ.type === 'experience') && (
                      <div className="space-y-4">
                        {currentQ.options.map((opt) => {
                          const isSelected = answers[currentQ.key] === (opt.value || opt.id);
                          return (
                            <motion.button
                              key={opt.id}
                              onClick={() => {
                                handleAnswer(opt.value || opt.id);
                                confetti({
                                  particleCount: 40,
                                  spread: 50,
                                  origin: { y: 0.6 }
                                });
                              }}
                              whileHover={{ scale: 1.03, x: 5 }}
                              whileTap={{ scale: 0.97 }}
                              className={`w-full p-6 text-left transition-all rounded-2xl border-3 ${
                                isSelected
                                  ? 'bg-gradient-to-r from-[#FFCC01] to-[#FFEE88] border-[#FFCC01] shadow-2xl'
                                  : 'bg-white/60 backdrop-blur-sm border-[#00DD70]/40 hover:border-[#FFCC01]'
                              }`}
                            >
                              <div className="flex items-center gap-4">
                                {opt.icon && <div className="text-4xl">{opt.icon}</div>}
                                {opt.emoji && <div className="text-4xl">{opt.emoji}</div>}
                                <div className="flex-1">
                                  <div className={`font-bold ${isSelected ? 'text-[#004543]' : 'text-[#004543]'} text-lg`}>{opt.label}</div>
                                  {opt.desc && <div className={`text-sm mt-1 font-bold ${isSelected ? 'text-gray-700' : 'text-gray-600'}`}>{opt.desc}</div>}
                                </div>
                                {isSelected && <div className="text-3xl">✅</div>}
                              </div>
                            </motion.button>
                          );
                        })}
                      </div>
                    )}

                    {/* Boolean */}
                    {currentQ.type === 'boolean' && (
                      <div className="space-y-4">
                        <div className="grid grid-cols-2 gap-6">
                          <motion.button
                            onClick={() => {
                              handleAnswer(true);
                              confetti({
                                particleCount: 80,
                                spread: 70,
                                origin: { y: 0.6 },
                                colors: ['#00DD70', '#B5FECC']
                              });
                            }}
                            whileHover={{ scale: 1.08, rotate: 3 }}
                            whileTap={{ scale: 0.95 }}
                            className={`p-8 text-center transition-all rounded-3xl border-4 ${
                              answers[currentQ.key] === true
                                ? 'bg-gradient-to-br from-[#00DD70] to-[#B5FECC] border-[#00DD70] shadow-2xl'
                                : 'bg-white/60 backdrop-blur-sm border-[#00DD70]/30 hover:border-[#00DD70]'
                            }`}
                          >
                            <div className="text-6xl mb-3">✅</div>
                            <div className="font-bold text-[#004543] text-lg">Sim, tenho!</div>
                          </motion.button>
                          <motion.button
                            onClick={() => {
                              handleAnswer(false);
                              confetti({
                                particleCount: 40,
                                spread: 50,
                                origin: { y: 0.6 },
                                colors: ['#FFCC01', '#FFEE88']
                              });
                            }}
                            whileHover={{ scale: 1.08, rotate: -3 }}
                            whileTap={{ scale: 0.95 }}
                            className={`p-8 text-center transition-all rounded-3xl border-4 ${
                              answers[currentQ.key] === false
                                ? 'bg-gradient-to-br from-[#FFCC01] to-[#FFEE88] border-[#FFCC01] shadow-2xl'
                                : 'bg-white/60 backdrop-blur-sm border-[#FFCC01]/30 hover:border-[#FFCC01]'
                            }`}
                          >
                            <div className="text-6xl mb-3">❌</div>
                            <div className="font-bold text-[#004543] text-lg">Ainda não</div>
                          </motion.button>
                        </div>
                        {currentQ.explanation && (
                          <motion.p
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            transition={{ delay: 0.3 }}
                            className="text-sm text-gray-700 text-center font-bold bg-[#B5FECC]/30 p-3 rounded-xl border border-[#00DD70]/30"
                          >
                            {currentQ.explanation}
                          </motion.p>
                        )}
                      </div>
                    )}

                    {/* Next button */}
                    <div className="text-center mt-8">
                      <button
                        onClick={handleNext}
                        disabled={
                          (currentQ.multiple && (!answers[currentQ.key] || answers[currentQ.key].length === 0)) ||
                          (!currentQ.multiple && !answers[currentQ.key] && answers[currentQ.key] !== false && answers[currentQ.key] !== 0)
                        }
                        className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-10 py-4 rounded-full font-bold shadow-xl hover:scale-105 transition-transform disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:scale-100"
                      >
                        {currentQuestion === questions.length - 1 ? 'Descobrir meu perfil! 🎯' : 'Próxima pergunta! →'}
                      </button>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
