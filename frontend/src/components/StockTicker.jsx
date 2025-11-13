import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

export default function StockTicker() {
  const [stocks, setStocks] = useState([
    { symbol: 'IBOV', name: 'Ibovespa', price: 125847.32, change: 1.24, changePercent: 0.99 },
    { symbol: 'PETR4', name: 'Petrobras', price: 38.42, change: 0.87, changePercent: 2.32 },
    { symbol: 'VALE3', name: 'Vale', price: 61.15, change: -0.45, changePercent: -0.73 },
    { symbol: 'ITUB4', name: 'Itaú', price: 27.83, change: 0.32, changePercent: 1.16 },
    { symbol: 'BBAS3', name: 'Banco do Brasil', price: 26.54, change: 0.18, changePercent: 0.68 },
    { symbol: 'WEGE3', name: 'WEG', price: 42.91, change: 0.76, changePercent: 1.80 },
    { symbol: 'B3SA3', name: 'B3', price: 11.24, change: -0.12, changePercent: -1.06 },
    { symbol: 'MGLU3', name: 'Magazine Luiza', price: 2.47, change: 0.08, changePercent: 3.35 },
    { symbol: '^GSPC', name: 'S&P 500', price: 4783.45, change: 23.87, changePercent: 0.50 },
    { symbol: '^DJI', name: 'Dow Jones', price: 37440.34, change: -58.32, changePercent: -0.16 },
    { symbol: 'BTC-USD', name: 'Bitcoin', price: 43287.50, change: 521.34, changePercent: 1.22 },
    { symbol: 'USDBRL', name: 'Dólar', price: 4.9823, change: 0.0134, changePercent: 0.27 },
  ]);

  // Simulate real-time price updates
  useEffect(() => {
    const interval = setInterval(() => {
      setStocks(prevStocks =>
        prevStocks.map(stock => {
          // Random price fluctuation (-0.5% to +0.5%)
          const fluctuation = (Math.random() - 0.5) * 0.01;
          const newPrice = stock.price * (1 + fluctuation);
          const newChange = newPrice - stock.price + stock.change;
          const newChangePercent = (newChange / stock.price) * 100;

          return {
            ...stock,
            price: newPrice,
            change: newChange,
            changePercent: newChangePercent,
          };
        })
      );
    }, 3000); // Update every 3 seconds

    return () => clearInterval(interval);
  }, []);

  // Duplicate stocks array for seamless infinite scroll
  const duplicatedStocks = [...stocks, ...stocks];

  return (
    <div className="relative w-full overflow-hidden bg-dark-card/50 backdrop-blur-md border-y border-dark-border py-3">
      {/* Gradient overlays for fade effect */}
      <div className="absolute left-0 top-0 bottom-0 w-20 bg-gradient-to-r from-dark-card/50 to-transparent z-10" />
      <div className="absolute right-0 top-0 bottom-0 w-20 bg-gradient-to-l from-dark-card/50 to-transparent z-10" />

      {/* Scrolling ticker */}
      <motion.div
        className="flex gap-8"
        animate={{
          x: [0, -50 * stocks.length * 8], // Adjust based on item width
        }}
        transition={{
          x: {
            repeat: Infinity,
            repeatType: "loop",
            duration: 60, // Slower scroll for readability
            ease: "linear",
          },
        }}
      >
        {duplicatedStocks.map((stock, index) => (
          <div
            key={`${stock.symbol}-${index}`}
            className="flex items-center gap-3 whitespace-nowrap flex-shrink-0"
          >
            {/* Symbol */}
            <div className="flex items-center gap-2">
              <span className="text-sm font-bold text-dark-text">{stock.symbol}</span>
              {stock.symbol.includes('BTC') && <span className="text-lg">₿</span>}
              {stock.symbol === 'USDBRL' && <span className="text-lg">💵</span>}
              {stock.symbol === 'IBOV' && <span className="text-lg">🇧🇷</span>}
            </div>

            {/* Price */}
            <span className="text-sm font-semibold text-dark-text">
              {stock.symbol === 'USDBRL' || stock.symbol.includes('BTC')
                ? stock.price.toFixed(2)
                : stock.price.toLocaleString('pt-BR', {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                  })}
            </span>

            {/* Change */}
            <span
              className={`text-xs font-medium px-2 py-1 rounded ${
                stock.changePercent >= 0
                  ? 'bg-success/20 text-success'
                  : 'bg-danger/20 text-danger'
              }`}
            >
              {stock.changePercent >= 0 ? '▲' : '▼'}{' '}
              {Math.abs(stock.changePercent).toFixed(2)}%
            </span>

            {/* Divider */}
            <div className="w-px h-6 bg-dark-border" />
          </div>
        ))}
      </motion.div>
    </div>
  );
}
