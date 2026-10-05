import React from 'react';

export default function OutputPanel({ output, exitCode, error }) {
  return (
    <div style={{ backgroundColor: '#000', color: '#0f0', padding: '15px', fontFamily: 'var(--font-mono)', minHeight: '200px' }}>
      {output && output.map((line, i) => (
        <div key={i} className="output-line">{line}</div>
      ))}
      
      {error && error.phase === 'runtime' && (
        <div style={{ color: 'var(--error-color)', marginTop: '10px' }}>
          {error.formatted}
        </div>
      )}
      
      {exitCode !== null && exitCode !== undefined && (
        <div style={{ color: '#888', marginTop: '20px' }}>
          Program exited with code {exitCode}
        </div>
      )}
    </div>
  );
}
