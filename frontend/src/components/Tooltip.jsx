import { useState } from 'react';

export default function Tooltip({ children, content }) {
  const [isVisible, setIsVisible] = useState(false);

  if (!content) return children;

  return (
    <div className="relative inline-block">
      <div
        onMouseEnter={() => setIsVisible(true)}
        onMouseLeave={() => setIsVisible(false)}
        className="cursor-help"
      >
        {children}
      </div>
      {isVisible && (
        <div className="absolute z-50 bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 text-xs text-white bg-academic-text rounded-lg shadow-lg w-64 pointer-events-none">
          <div className="relative">
            {content}
            <div className="absolute top-full left-1/2 transform -translate-x-1/2 -mt-1">
              <div className="border-4 border-transparent border-t-academic-text"></div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
