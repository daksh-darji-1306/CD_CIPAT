import React, { useCallback, useState, useEffect, useRef } from 'react';
import Tree from 'react-d3-tree';

const nodeWidth = 240;
const nodeHeight = 70;

export default function AstTree({ ast }) {
  const [orientation, setOrientation] = useState('vertical');
  const [translate, setTranslate] = useState({ x: 300, y: 80 });
  const containerElemRef = useRef(null);

  const updateTranslate = useCallback(() => {
    if (containerElemRef.current) {
      const { width, height } = containerElemRef.current.getBoundingClientRect();
      if (orientation === 'vertical') {
        setTranslate({ x: width / 2, y: 100 });
      } else {
        setTranslate({ x: 120, y: height / 2 });
      }
    }
  }, [orientation]);

  const containerRef = useCallback((elem) => {
    containerElemRef.current = elem;
    updateTranslate();
  }, [updateTranslate]);

  useEffect(() => {
    updateTranslate();
    window.addEventListener('resize', updateTranslate);
    return () => window.removeEventListener('resize', updateTranslate);
  }, [updateTranslate]);

  if (!ast) return null;
  
  // Premium vibrant card design for AST Nodes
  const renderCustomNodeElement = ({ nodeDatum, toggleNode }) => {
    const isLeaf = !nodeDatum.children || nodeDatum.children.length === 0;

    // Internal nodes get a deep glass effect with a pink/purple glow, leaves get a vibrant cyan/blue mesh
    const nodeBg = isLeaf 
      ? 'linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%)'
      : 'linear-gradient(145deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%)';
    
    const nodeBorder = isLeaf
      ? '1px solid rgba(255, 255, 255, 0.4)'
      : '1px solid rgba(236, 72, 153, 0.5)';
      
    const nodeShadow = isLeaf
      ? '0 10px 25px -5px rgba(59, 130, 246, 0.5), 0 8px 10px -6px rgba(59, 130, 246, 0.5)'
      : '0 10px 25px -5px rgba(236, 72, 153, 0.3), inset 0 1px 1px rgba(255, 255, 255, 0.1)';

    return (
      <g>
        <foreignObject x={-nodeWidth / 2} y={-nodeHeight / 2} width={nodeWidth} height={nodeHeight}>
          <div 
            onClick={toggleNode}
            style={{
              width: '100%',
              height: '100%',
              background: nodeBg,
              backdropFilter: 'blur(12px)',
              borderRadius: '16px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: nodeShadow,
              border: nodeBorder,
              color: '#ffffff',
              fontFamily: '"Inter", system-ui, sans-serif',
              fontSize: '16px',
              fontWeight: isLeaf ? '700' : '600',
              letterSpacing: '0.5px',
              cursor: 'pointer',
              userSelect: 'none',
              padding: '0 16px',
              textAlign: 'center',
              boxSizing: 'border-box',
              transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-4px) scale(1.03)';
              e.currentTarget.style.boxShadow = isLeaf 
                ? '0 20px 30px -10px rgba(59, 130, 246, 0.7), 0 0 15px rgba(6, 182, 212, 0.5)' 
                : '0 20px 30px -10px rgba(236, 72, 153, 0.5), 0 0 15px rgba(236, 72, 153, 0.4)';
              e.currentTarget.style.border = isLeaf 
                ? '1px solid rgba(255, 255, 255, 0.8)' 
                : '1px solid rgba(236, 72, 153, 0.9)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0) scale(1)';
              e.currentTarget.style.boxShadow = nodeShadow;
              e.currentTarget.style.border = nodeBorder;
            }}
          >
            <div style={{
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              whiteSpace: 'nowrap',
              textShadow: '0 2px 4px rgba(0,0,0,0.5)'
            }}>
              {nodeDatum.name}
            </div>
          </div>
        </foreignObject>
      </g>
    );
  };

  const btnStyle = {
    padding: '8px 16px',
    borderRadius: '8px',
    border: 'none',
    color: '#fff',
    fontWeight: '600',
    fontSize: '14px',
    cursor: 'pointer',
    transition: 'all 0.2s ease',
    fontFamily: '"Inter", system-ui, sans-serif',
  };

  return (
    <div ref={containerRef} style={{ 
      width: '100%', 
      height: '100%', 
      position: 'relative',
      background: 'radial-gradient(circle at top right, #1e1b4b, #020617 60%)', 
      borderRadius: '16px', 
      overflow: 'hidden', 
      border: '1px solid rgba(255, 255, 255, 0.1)',
      boxShadow: 'inset 0 0 60px rgba(0,0,0,0.8)'
    }}>
      
      {/* Removed the SVG defs since gradients on straight lines cause a 0-width bounding box bug in Chrome */}

      <style>
        {`
          .fancy-link {
            stroke: #ec4899 !important;
            stroke-width: 3px !important;
            opacity: 0.6;
            transition: stroke-width 0.3s, opacity 0.3s, stroke 0.3s;
            filter: drop-shadow(0 0 4px rgba(236, 72, 153, 0.6));
          }
          .fancy-link:hover {
            stroke: #3b82f6 !important;
            stroke-width: 5px !important;
            opacity: 1;
            filter: drop-shadow(0 0 8px rgba(59, 130, 246, 0.9));
          }
        `}
      </style>
      
      <div style={{
        position: 'absolute',
        top: '20px',
        right: '20px',
        display: 'flex',
        background: 'rgba(15, 23, 42, 0.6)',
        backdropFilter: 'blur(12px)',
        borderRadius: '10px',
        padding: '6px',
        border: '1px solid rgba(255, 255, 255, 0.1)',
        zIndex: 10,
        gap: '6px',
        boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)'
      }}>
        <button 
          onClick={() => setOrientation('vertical')}
          style={{ ...btnStyle, background: orientation === 'vertical' ? 'rgba(59, 130, 246, 0.8)' : 'transparent' }}
        >
          Vertical
        </button>
        <button 
          onClick={() => setOrientation('horizontal')}
          style={{ ...btnStyle, background: orientation === 'horizontal' ? 'rgba(59, 130, 246, 0.8)' : 'transparent' }}
        >
          Horizontal
        </button>
      </div>

      <Tree 
        data={ast} 
        orientation={orientation}
        pathFunc="diagonal"
        translate={translate}
        nodeSize={orientation === 'vertical' ? { x: 280, y: 160 } : { x: 320, y: 140 }}
        renderCustomNodeElement={renderCustomNodeElement}
        pathClassFunc={() => 'fancy-link'}
        separation={{ siblings: 1.1, nonSiblings: 1.3 }}
      />
    </div>
  );
}
