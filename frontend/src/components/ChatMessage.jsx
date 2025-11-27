import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';

export default function ChatMessage({ message, isTyping = false, delay = 0 }) {
  const [displayedText, setDisplayedText] = useState('');
  const [isComplete, setIsComplete] = useState(false);

  useEffect(() => {
    if (!isTyping) {
      setDisplayedText(message);
      setIsComplete(true);
      return;
    }

    let currentIndex = 0;
    const timer = setTimeout(() => {
      const interval = setInterval(() => {
        if (currentIndex <= message.length) {
          setDisplayedText(message.slice(0, currentIndex));
          currentIndex++;
        } else {
          clearInterval(interval);
          setIsComplete(true);
        }
      }, 30);
      return () => clearInterval(interval);
    }, delay);

    return () => clearTimeout(timer);
  }, [message, isTyping, delay]);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: delay / 1000 }}
      className="flex items-start gap-3 mb-4"
    >
      {/* Avatar do Breno */}
      <div className="flex-shrink-0 w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white font-bold shadow-lg text-sm">
        B
      </div>

      {/* Balão de mensagem */}
      <div className="flex-1 bg-white border border-blue-100 rounded-2xl rounded-tl-none p-4 shadow-sm">
        <p className="text-slate-700 leading-relaxed font-medium">
          {displayedText}
          {isTyping && !isComplete && (
            <span className="inline-block w-1 h-4 ml-1 bg-blue-600 animate-pulse" />
          )}
        </p>
      </div>
    </motion.div>
  );
}
