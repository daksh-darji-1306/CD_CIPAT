import React, { useState } from 'react';

export default function TacView({ tac, optimizedTac, stats, log, optimize }) {
  const [showLog, setShowLog] = useState(false);

  if (!tac || tac.length === 0) {
    return <div className="empty-state">No TAC generated.</div>;
  }

  const renderTac = (lines) => {
    return lines.map((line, i) => (
      <div key={i} className="tac-line">
        <span className="tac-line-num">{i + 1}</span>
        <span>{line}</span>
      </div>
    ));
  };

  return (
    <div>
      {stats && (
        <div className="stats-chip">
          {stats.tac_before} &rarr; {stats.tac_after} instructions 
          ({Math.round((1 - stats.tac_after / stats.tac_before) * 100)}% fewer)
        </div>
      )}
      
      <div className="tac-container">
        <div className="tac-column">
          <h3>Unoptimized TAC</h3>
          <div style={{ backgroundColor: '#1a1a1a', padding: '10px', borderRadius: '4px' }}>
            {renderTac(tac)}
          </div>
        </div>
        
        {optimize && (
          <div className="tac-column">
            <h3>Optimized TAC</h3>
            <div style={{ backgroundColor: '#1a1a1a', padding: '10px', borderRadius: '4px' }}>
              {optimizedTac && optimizedTac.length > 0 ? renderTac(optimizedTac) : <i>No optimized TAC</i>}
            </div>
          </div>
        )}
      </div>

      {optimize && log && log.length > 0 && (
        <div style={{ marginTop: '20px' }}>
          <h3 style={{ cursor: 'pointer', color: 'var(--accent-color)' }} onClick={() => setShowLog(!showLog)}>
            Optimization Log {showLog ? '[-]' : '[+]'}
          </h3>
          {showLog && (
            <div>
              {log.map((entry, idx) => (
                <div key={idx} style={{ marginBottom: '15px' }}>
                  <strong>Iteration {entry.iteration}: {entry.pass}</strong>
                  <div style={{ backgroundColor: '#1a1a1a', padding: '5px 10px', marginTop: '5px' }}>
                    {renderTac(entry.tac)}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
