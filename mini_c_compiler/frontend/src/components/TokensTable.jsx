import React from 'react';

export default function TokensTable({ tokens }) {
  if (!tokens || tokens.length === 0) return null;
  
  return (
    <table>
      <thead>
        <tr>
          <th>#</th>
          <th>Type</th>
          <th>Lexeme</th>
          <th>Line</th>
          <th>Col</th>
        </tr>
      </thead>
      <tbody>
        {tokens.map((t, i) => (
          <tr key={i}>
            <td>{i + 1}</td>
            <td><span className={`token-badge token-${t.type}`}>{t.type}</span></td>
            <td><code>{t.lexeme}</code></td>
            <td>{t.line}</td>
            <td>{t.col}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
