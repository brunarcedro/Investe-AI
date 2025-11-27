import { motion } from 'framer-motion';

export default function UserMessageButton({ text, onClick, selected = false }) {
  return (
    <div className="flex justify-end mb-4">
      <motion.button
        onClick={onClick}
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        className={`max-w-[80%] px-6 py-4 rounded-2xl rounded-tr-none shadow-lg font-medium transition-all ${
          selected
            ? 'bg-gradient-to-br from-blue-600 to-indigo-600 text-white border-2 border-blue-600'
            : 'bg-white text-slate-800 border-2 border-blue-200 hover:bg-blue-50'
        }`}
      >
        {text}
      </motion.button>
    </div>
  );
}
