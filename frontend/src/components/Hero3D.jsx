import { Suspense, lazy } from 'react';
import { motion } from 'framer-motion';

// Lazy load Spline to improve initial load performance
const Spline = lazy(() => import('@splinetool/react-spline'));

export default function Hero3D() {
  return (
    <div className="relative w-full h-[600px] overflow-hidden rounded-2xl">
      {/* Fallback gradient background */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary/20 via-gradient-purple/10 to-gradient-cyan/20" />

      {/* 3D Scene */}
      <Suspense
        fallback={
          <div className="absolute inset-0 flex items-center justify-center">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
              className="text-6xl"
            >
              💎
            </motion.div>
          </div>
        }
      >
        {/* Placeholder for Spline scene - você pode criar sua própria cena em https://spline.design/ */}
        <div className="absolute inset-0 flex items-center justify-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 1 }}
            className="text-center"
          >
            <motion.div
              animate={{
                y: [0, -20, 0],
                rotateY: [0, 180, 360],
              }}
              transition={{
                duration: 4,
                repeat: Infinity,
                ease: "easeInOut",
              }}
              className="text-9xl mb-6 drop-shadow-2xl"
            >
              💎
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="space-y-4"
            >
              <h2 className="text-4xl font-bold bg-gradient-to-r from-primary via-gradient-purple to-gradient-cyan bg-clip-text text-transparent">
                Investimentos Inteligentes
              </h2>
              <p className="text-xl text-dark-muted max-w-md mx-auto">
                Powered by Neural Networks & Machine Learning
              </p>
            </motion.div>

            {/* Floating particles */}
            {[...Array(20)].map((_, i) => (
              <motion.div
                key={i}
                initial={{
                  x: Math.random() * 600 - 300,
                  y: Math.random() * 600 - 300,
                  opacity: 0,
                }}
                animate={{
                  y: [Math.random() * 600 - 300, Math.random() * 600 - 300],
                  opacity: [0, 0.6, 0],
                }}
                transition={{
                  duration: 3 + Math.random() * 2,
                  repeat: Infinity,
                  delay: Math.random() * 2,
                }}
                className="absolute w-2 h-2 rounded-full bg-primary"
                style={{
                  left: '50%',
                  top: '50%',
                }}
              />
            ))}
          </motion.div>
        </div>

        {/*
          Para adicionar uma cena Spline real:
          1. Vá em https://spline.design/
          2. Crie sua cena 3D (ex: gráficos 3D, moedas flutuantes, etc)
          3. Exporte como React Component
          4. Cole o código aqui:

          <Spline
            scene="https://prod.spline.design/SEU-ID-AQUI/scene.splinecode"
            className="absolute inset-0"
          />
        */}
      </Suspense>

      {/* Overlay gradient for better text readability */}
      <div className="absolute inset-0 bg-gradient-to-t from-dark-bg via-transparent to-transparent pointer-events-none" />
    </div>
  );
}
