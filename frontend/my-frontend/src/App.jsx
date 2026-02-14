import React, { useState } from 'react';

function SessionManager() {
  const [userId, setUserId] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const createSession = async () => {
    if (!userId) {
      alert("Please enter a User ID");
      return;
    }

    setLoading(true);
    setMessage('');

    try {
      // Replace with your AWS Public IP
      const response = await fetch('http://44.249.61.11:8000/createSessionsPerUser', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ userId: userId }),
      });

      const data = await response.json();

      if (response.ok) {
        // Success message as requested
        setMessage(`session created to user: ${data.sessionId}`);
      } else {
        setMessage(`Error: ${data.error || 'Failed to create session'}`);
      }
    } catch (error) {
      setMessage('Network error: Is the backend running?');
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '40px', fontFamily: 'sans-serif' }}>
      <h2>User Session Creator</h2>
      
      <input
        type="text"
        placeholder="Enter User ID (e.g., 12345)"
        value={userId}
        onChange={(e) => setUserId(e.target.value)}
        style={{ padding: '8px', marginRight: '10px' }}
      />

      <button 
        onClick={createSession} 
        disabled={loading}
        style={{ padding: '8px 16px', cursor: 'pointer' }}
      >
        {loading ? 'Processing...' : 'Create Session'}
      </button>

      {message && (
        <div style={{ marginTop: '20px', color: message.includes('Error') ? 'red' : 'green' }}>
          <strong>{message}</strong>
        </div>
      )}
    </div>
  );
}

export default SessionManager;