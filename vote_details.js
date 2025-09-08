import { useState, useEffect } from 'react';

export default function Home() {
  const [votes, setVotes] = useState(0);
  const [loading, setLoading] = useState(true);

  const fetchVotes = async () => {
    const res = await fetch('/api/votes');
    const data = await res.json();
    setVotes(data.votes);
    setLoading(false);
  };

  const updateVotes = async (newVotes) => {
    const res = await fetch('/api/votes', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ votes: newVotes }),
    });

    const data = await res.json();
    setVotes(data.votes);
  };

  useEffect(() => {
    fetchVotes();
  }, []);

  if (loading) return <p>Loading vote count...</p>;

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>Votes: {votes}</h1>
      <button onClick={() => updateVotes(votes + 1)}>⬆️ Upvote</button>
      <button onClick={() => updateVotes(votes - 1)} style={{ marginLeft: '10px' }}>
        ⬇️ Downvote
      </button>
    </div>
  );
}
