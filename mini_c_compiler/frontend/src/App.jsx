import React, { useState, useEffect } from 'react';
import Split from 'react-split';
import { getExamples, compile } from './api';
import Editor from './components/Editor';
import PipelineBar from './components/PipelineBar';
import TokensTable from './components/TokensTable';
import AstTree from './components/AstTree';
import SymbolTable from './components/SymbolTable';
import TacView from './components/TacView';
import OutputPanel from './components/OutputPanel';
import ErrorBanner from './components/ErrorBanner';

function App() {
  const [examples, setExamples] = useState([]);
  const [source, setSource] = useState("");
  const [optimize, setOptimize] = useState(true);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [activeTab, setActiveTab] = useState('Output');
  const [errorLine, setErrorLine] = useState(null);
  const [globalError, setGlobalError] = useState(null);

  useEffect(() => {
    getExamples().then(data => {
      setExamples(data);
      if (data.length > 0) setSource(data[0].source);
    }).catch(err => {
      setGlobalError(err.message);
    });
  }, []);

  const handleRun = async () => {
    setLoading(true);
    setGlobalError(null);
    setErrorLine(null);
    try {
      const res = await compile(source, optimize);
      setResult(res);
      if (res.success) {
        setActiveTab('Output');
      } else {
        if (res.error) {
          setErrorLine(res.error.line);
          const phaseTabMap = {
            'lexical': 'Tokens',
            'syntax': 'AST',
            'semantic': 'Symbol Table',
            'codegen': 'TAC',
            'optimizer': 'TAC',
            'runtime': 'Output'
          };
          setActiveTab(phaseTabMap[res.error.phase] || 'Output');
        }
      }
    } catch (err) {
      setGlobalError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.ctrlKey && e.key === 'Enter') {
        handleRun();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  });

  const handleExampleChange = (e) => {
    const ex = examples.find(ex => ex.id === e.target.value);
    if (ex) {
      setSource(ex.source);
      setResult(null);
      setErrorLine(null);
      setGlobalError(null);
    }
  };

  const tabs = ['Tokens', 'AST', 'Symbol Table', 'TAC', 'Output'];
  
  const renderTabContent = () => {
    if (!result) return <div className="empty-state">Run the compiler to see results.</div>;
    
    // Determine if phase was skipped
    const checkSkipped = (phaseName) => {
      if (result.phases[phaseName] === 'skipped') {
        return <div className="empty-state">This phase did not run because of an earlier error.</div>;
      }
      return null;
    };

    switch (activeTab) {
      case 'Tokens':
        return checkSkipped('lexical') || <TokensTable tokens={result.tokens} />;
      case 'AST':
        return checkSkipped('syntax') || <AstTree ast={result.ast} />;
      case 'Symbol Table':
        return checkSkipped('semantic') || <SymbolTable symbols={result.symbol_table} />;
      case 'TAC':
        return checkSkipped('codegen') || 
          <TacView 
            tac={result.tac} 
            optimizedTac={result.optimized_tac} 
            stats={result.stats} 
            log={result.optimization_log}
            optimize={optimize}
          />;
      case 'Output':
        return checkSkipped('execution') || 
          <OutputPanel 
            output={result.output} 
            exitCode={result.exit_code} 
            error={result.error} 
          />;
      default:
        return null;
    }
  };

  return (
    <div className="app-container">
      <header>
        <div>
          <h1>Mini C Compiler</h1>
          <div className="subtitle">Compiler Design (3170701) - CIPAT Activity 2</div>
        </div>
      </header>
      
      {globalError && <div className="error-banner">{globalError}</div>}
      
      <div className="toolbar">
        <select onChange={handleExampleChange}>
          <option value="">-- Load Example --</option>
          {examples.map(ex => (
            <option key={ex.id} value={ex.id}>{ex.name}</option>
          ))}
        </select>
        
        <label style={{ display: 'flex', alignItems: 'center', gap: '5px', cursor: 'pointer' }}>
          <input 
            type="checkbox" 
            checked={optimize} 
            onChange={e => setOptimize(e.target.checked)} 
          />
          Optimize
        </label>
        
        <button 
          className="primary" 
          onClick={handleRun} 
          disabled={loading}
          title="Ctrl+Enter"
        >
          {loading ? 'Running...' : 'Run'}
        </button>
        
        <button onClick={() => {
          setSource("");
          setResult(null);
          setErrorLine(null);
          setGlobalError(null);
        }}>
          Clear
        </button>
      </div>
      
      {result && result.error && (
        <ErrorBanner error={result.error} onErrorClick={(line) => setErrorLine(line)} />
      )}
      
      <Split 
        className="main-content" 
        sizes={[35, 65]} 
        minSize={[200, 300]} 
        gutterSize={8}
        snapOffset={30}
      >
        <div className="left-pane">
          <Editor source={source} setSource={setSource} errorLine={errorLine} />
        </div>
        
        <div className="right-pane">
          <PipelineBar phases={result ? result.phases : {}} />
          
          <div className="tabs-header">
            {tabs.map(tab => (
              <button 
                key={tab}
                className={`tab-btn ${activeTab === tab ? 'active' : ''}`}
                onClick={() => setActiveTab(tab)}
              >
                {tab}
              </button>
            ))}
          </div>
          
          <div className="tab-content">
            {renderTabContent()}
          </div>
        </div>
      </Split>
    </div>
  );
}

export default App;
