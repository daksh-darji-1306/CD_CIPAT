import React from 'react';

export default function PipelineBar({ phases }) {
  const getPhaseClass = (status) => {
    if (status === 'ok') return 'ok';
    if (status === 'error') return 'error';
    return '';
  };

  const steps = [
    { key: 'lexical', label: 'Lexical' },
    { key: 'syntax', label: 'Syntax' },
    { key: 'semantic', label: 'Semantic' },
    { key: 'codegen', label: 'Code Gen' },
    { key: 'optimizer', label: 'Optimizer' },
    { key: 'execution', label: 'Execution' }
  ];

  return (
    <div className="pipeline-bar">
      {steps.map(step => (
        <div key={step.key} className={`pipeline-phase ${getPhaseClass(phases[step.key])}`}>
          {step.label}
        </div>
      ))}
    </div>
  );
}
