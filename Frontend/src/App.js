import React, { useState } from 'react';

function App() {
  const [text, setText] = useState('');
  const [incidents, setIncidents] = useState([]);

  const handleAnalyze = async () => {
    if (!text) return;
    const response = await fetch('/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ raw_text: text, source: 'Dispatcher Input' })
    });
    const data = await response.json();
    setIncidents([data, ...incidents]);
    setText('');
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>🚨 SirenPrep AI Dispatcher Dashboard</h1>
      <div style={{ marginBottom: '20px' }}>
        <textarea 
          rows="3" 
          cols="60" 
          value={text} 
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste distress message here (e.g., Water rising fast, 2 people trapped on roof near Main St)..."
        />
        <br/>
        <button onClick={handleAnalyze} style={{ padding: '10px 20px', cursor: 'pointer' }}>
          Process Distress Stream
        </button>
      </div>

      <h2>Live Triaged Incidents</h2>
      <table border="1" cellPadding="10" style={{ borderCollapse: 'collapse', width: '100%' }}>
        <thead>
          <tr style={{ background: '#f2f2f2' }}>
            <th>Priority Score</th>
            <th>Category</th>
            <th>Location</th>
            <th>Raw Message</th>
          </tr>
        </thead>
        <tbody>
          {incidents.map((inc, i) => (
            <tr key={i} style={{ backgroundColor: inc.priority_score >= 8 ? '#ffcccc' : '#fff' }}>
              <td><strong>{inc.priority_score} / 10</strong></td>
              <td>{inc.category}</td>
              <td>{inc.location_text}</td>
              <td>{inc.raw_text}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
