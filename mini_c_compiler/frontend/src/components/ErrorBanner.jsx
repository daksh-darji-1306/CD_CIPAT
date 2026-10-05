import React from 'react';

export default function ErrorBanner({ error, onErrorClick }) {
  if (!error) return null;
  
  return (
    <div className="error-banner" onClick={() => onErrorClick(error.line)}>
      {error.formatted} (Click to focus line)
    </div>
  );
}
