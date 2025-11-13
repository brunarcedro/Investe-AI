import { Suspense, lazy } from 'react';
import { motion } from 'framer-motion';

// Lazy load Spline component for better performance
const Spline = lazy(() => import('@splinetool/react-spline'));

export default function Spline3D({ scene = 'default', className = '' }) {
  // Spline scenes URLs - você pode criar suas próprias cenas em https://spline.design/
  const scenes = {
    // Placeholder - você precisará criar cenas 3D no Spline e exportar os URLs
    default: 'https://prod.spline.design/6Wq1Q7YGyM-iab9i/scene.splinecode', // Exemplo de cena 3D
    hero: 'https://prod.spline.design/6Wq1Q7YGyM-iab9i/scene.splinecode',
    portfolio: 'https://prod.spline.design/6Wq1Q7YGyM-iab9i/scene.splinecode',
  };

  return (
    <div className={`relative ${className}`}>
      <Suspense
        fallback={
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="w-full h-full flex items-center justify-center bg-dark-card/30 rounded-2xl backdrop-blur-sm"
          >
            <div className="text-center">
              <div className="text-6xl mb-4 animate-spin">💎</div>
              <p className="text-dark-muted">Carregando visualização 3D...</p>
            </div>
          </motion.div>
        }
      >
        <Spline
          scene={scenes[scene] || scenes.default}
          className="w-full h-full"
        />
      </Suspense>
    </div>
  );
}

// Componente alternativo usando CSS 3D transforms para não depender de Spline externo
export function CSS3DCard({ children, className = '' }) {
  return (
    <motion.div
      className={`relative ${className}`}
      style={{
        transformStyle: 'preserve-3d',
        perspective: '1000px',
      }}
      whileHover={{
        rotateY: 5,
        rotateX: 5,
      }}
      transition={{ duration: 0.3 }}
    >
      <div
        className="relative glass-card p-8"
        style={{
          transformStyle: 'preserve-3d',
          transform: 'translateZ(50px)',
        }}
      >
        {children}

        {/* Camadas 3D de profundidade */}
        <div
          className="absolute inset-0 bg-gradient-to-br from-primary/10 to-gradient-purple/10 rounded-2xl -z-10"
          style={{
            transform: 'translateZ(-20px)',
          }}
        />
        <div
          className="absolute inset-0 bg-gradient-to-br from-gradient-cyan/5 to-primary/5 rounded-2xl -z-20"
          style={{
            transform: 'translateZ(-40px)',
          }}
        />
      </div>
    </motion.div>
  );
}

// Componente de partículas flutuantes 3D (alternativa leve)
export function FloatingParticles({ count = 20 }) {
  const particles = Array.from({ length: count }, (_, i) => ({
    id: i,
    size: Math.random() * 4 + 2,
    x: Math.random() * 100,
    y: Math.random() * 100,
    duration: Math.random() * 10 + 10,
    delay: Math.random() * 5,
  }));

  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {particles.map((particle) => (
        <motion.div
          key={particle.id}
          className="absolute rounded-full bg-gradient-to-r from-primary/30 to-gradient-cyan/30 blur-sm"
          style={{
            width: particle.size,
            height: particle.size,
            left: `${particle.x}%`,
            top: `${particle.y}%`,
          }}
          animate={{
            y: [0, -30, 0],
            x: [0, Math.random() * 20 - 10, 0],
            opacity: [0.3, 0.6, 0.3],
            scale: [1, 1.2, 1],
          }}
          transition={{
            duration: particle.duration,
            delay: particle.delay,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        />
      ))}
    </div>
  );
}

// Componente de cubo 3D animado (CSS puro)
export function AnimatedCube({ className = '' }) {
  return (
    <div className={`relative ${className}`} style={{ perspective: '1000px' }}>
      <motion.div
        className="relative w-32 h-32"
        style={{ transformStyle: 'preserve-3d' }}
        animate={{
          rotateX: 360,
          rotateY: 360,
        }}
        transition={{
          duration: 20,
          repeat: Infinity,
          ease: 'linear',
        }}
      >
        {/* Faces do cubo */}
        {[
          { transform: 'rotateY(0deg) translateZ(64px)', bg: 'from-primary to-blue-600' },
          { transform: 'rotateY(90deg) translateZ(64px)', bg: 'from-gradient-purple to-purple-600' },
          { transform: 'rotateY(180deg) translateZ(64px)', bg: 'from-gradient-cyan to-cyan-600' },
          { transform: 'rotateY(-90deg) translateZ(64px)', bg: 'from-success to-green-600' },
          { transform: 'rotateX(90deg) translateZ(64px)', bg: 'from-warning to-orange-600' },
          { transform: 'rotateX(-90deg) translateZ(64px)', bg: 'from-danger to-red-600' },
        ].map((face, index) => (
          <div
            key={index}
            className={`absolute w-32 h-32 bg-gradient-to-br ${face.bg} opacity-70 border border-white/20`}
            style={{ transform: face.transform }}
          />
        ))}
      </motion.div>
    </div>
  );
}
