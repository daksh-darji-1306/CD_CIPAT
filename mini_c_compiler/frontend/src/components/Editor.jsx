import React, { useState, useRef } from 'react';

export default function Editor({ source, setSource, errorLine }) {
  const textareaRef = useRef(null);
  
  const handleKeyDown = (e) => {
    if (e.key === 'Tab') {
      e.preventDefault();
      const start = e.target.selectionStart;
      const end = e.target.selectionEnd;
      const newSource = source.substring(0, start) + "    " + source.substring(end);
      setSource(newSource);
      setTimeout(() => {
        if (textareaRef.current) {
          textareaRef.current.selectionStart = textareaRef.current.selectionEnd = start + 4;
        }
      }, 0);
    }
  };

  const lines = source.split('\n');

  return (
    <div className="editor-container">
      <div className="editor-gutter">
        {lines.map((_, i) => (
          <div 
            key={i} 
            className={`editor-gutter-line ${(i + 1) === errorLine ? 'error-line' : ''}`}
          >
            {i + 1}
          </div>
        ))}
      </div>
      <textarea 
        ref={textareaRef}
        className="editor-textarea" 
        value={source}
        onChange={(e) => setSource(e.target.value)}
        onKeyDown={handleKeyDown}
        spellCheck="false"
      />
    </div>
  );
}
