import React from 'react';

export default function SymbolTable({ symbols }) {
  if (!symbols || symbols.length === 0) {
    return <div className="empty-state">No symbols declared.</div>;
  }
  
  return (
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Unique Name</th>
          <th>Type</th>
          <th>Scope</th>
          <th>Line</th>
        </tr>
      </thead>
      <tbody>
        {symbols.map((sym, i) => (
          <tr key={i}>
            <td><code>{sym.name}</code></td>
            <td><code>{sym.unique_name}</code></td>
            <td>{sym.type}</td>
            <td>{sym.scope}</td>
            <td>{sym.line}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
