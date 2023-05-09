import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";
import FlashMessage from "./Messages";

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showFlashMessage, setShowFlashMessage] = useState("");
  const [flashMessage, setFlashMessage] = useState("");
  const [flashMessageType, setFlashMessageType] = useState("");
  const navigate = useNavigate();


  const handleSubmit = async (event) => {
    event.preventDefault();

    const params = new URLSearchParams();
    params.append('grant_type', 'password');
    params.append('username', username);
    params.append('password', password);


    const requestOptions = {
      method: "POST",
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      body: params,
    };

    const response = await fetch("http://167.172.166.15:8000/api/token", requestOptions);
    const data = await response.json()
    const token = data.token
    localStorage.setItem("token", token);
    console.log(data)

    if (!response.ok) {
      setFlashMessage(data.detail);
      setFlashMessageType("danger");
      setShowFlashMessage(true);
    } else {
      setFlashMessage("Logged in succesfully");
      setFlashMessageType("success");
      setShowFlashMessage(true);
    }
  

  };

  return (
    <div>
      {showFlashMessage && (
        <FlashMessage
            message={flashMessage}
            type={flashMessageType}
            onClose={() => setShowFlashMessage(false)}
        />
      )}
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="email">Username</label>
          <input
            type="username"
            id="username"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
          />
        </div>
        <div>
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
        </div>
        <FlashMessage message={flashMessage}></FlashMessage>
        <br></br>
        <button type="submit">Login</button>
      </form>
    </div>
  );
};


export default Login;
