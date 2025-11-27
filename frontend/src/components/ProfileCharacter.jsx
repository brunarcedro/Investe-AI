import { motion } from 'framer-motion';

export default function ProfileCharacter({ profile, onContinue }) {
  // profile agora é o objeto completo da API
  const perfilNome = typeof profile === 'string' ? profile : profile?.perfil || 'Moderado';

  // Cores por perfil
  const profileColors = {
    'Conservador': 'from-blue-500 to-blue-600',
    'Moderado': 'from-blue-600 to-indigo-600',
    'Agressivo': 'from-indigo-600 to-purple-600',
    'Muito Conservador': 'from-blue-400 to-blue-500',
    'Muito Arrojado': 'from-purple-600 to-pink-600',
    'Arrojado': 'from-indigo-500 to-purple-500'
  };

  const color = profileColors[perfilNome] || 'from-blue-600 to-indigo-600';

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="max-w-2xl w-full text-center"
      >
        {/* Breno Avatar Grande */}
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: 'spring', delay: 0.2 }}
          className="mb-8"
        >
          <div className="w-32 h-32 mx-auto rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white font-black text-6xl shadow-2xl mb-6">
            B
          </div>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
            className="text-2xl text-slate-800 font-bold"
          >
            Pronto! Já te conheço melhor 😊
          </motion.p>
        </motion.div>

        {/* Resultado */}
        <motion.div
          initial={{ y: 30, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.6 }}
          className="bg-white rounded-3xl p-8 mb-8 shadow-2xl border-2 border-blue-100"
        >
          <p className="text-slate-600 text-lg mb-4">Seu perfil de investidor é:</p>

          <motion.div
            initial={{ scale: 0.8 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.8, type: 'spring' }}
            className={`inline-block px-10 py-4 bg-gradient-to-r ${color} rounded-full mb-6 shadow-xl`}
          >
            <span className="text-3xl font-black text-white">
              {perfilNome}
            </span>
          </motion.div>

          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1 }}
            className="text-xl text-slate-800 leading-relaxed"
          >
            Agora vou montar uma <span className="text-blue-600 font-bold">carteira personalizada</span> especialmente pra você! 🎯
          </motion.p>
        </motion.div>

        {/* CTA */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.2 }}
        >
          <button
            onClick={onContinue}
            className="px-12 py-5 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-full font-black text-xl text-white shadow-2xl hover:scale-105 transition-transform"
          >
            Ver Minha Carteira! 💰
          </button>
          <p className="text-slate-500 text-sm mt-4">
            Preparando recomendações personalizadas...
          </p>
        </motion.div>
      </motion.div>
    </div>
  );
}
