import React, { useState } from 'react';
import { addUser } from '../services/api.js';

function AddUserPage() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await addUser({ username, email, password });
      // Show success message and reset form
    } catch (error) {
      // Handle error
    }
  };

  return (
    <div className="add-user-page">
      <h1>Add New User</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username"
          required
        />
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          required
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
        />
        <button type="submit">Add User</button>
      </form>
    </div>
  );
}

export default AddUserPage;