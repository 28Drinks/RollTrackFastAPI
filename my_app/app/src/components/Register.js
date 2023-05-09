import React, { useState } from "react";

import { useNavigate } from "react-router-dom";
import FlashMessage from "./Messages";


const Register = () => {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmationPassword, setConfirmationPassword] = useState("");
    const [showFlashMessage, setShowFlashMessage] = useState("");
    const [flashMessage, setFlashMessage] = useState("");
    const [flashMessageType, setFlashMessageType] = useState("");
    const navigate = useNavigate();


    const submitRegistration = async () => {
        const requestOptions = {
            method: "POST",
            headers: {"content-Type": "application/json"},
            body: JSON.stringify({ username: username, email: email, hashed_password: password}),
        };

        const response = await fetch('http://167.172.166.15:8000/api/register', requestOptions);
        const data = await response.json();

        if (!response.ok) {
            setFlashMessage(data.detail);
            setFlashMessageType("danger");
            setShowFlashMessage(true);
        } else {
            setFlashMessage("Registration succesfull, you may log in now");
            setFlashMessageType("success");
            setShowFlashMessage(true);
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (password === confirmationPassword ) {
            submitRegistration();
        } else {
            setFlashMessage("Ensure the passwords match");
            setFlashMessageType("danger");
            setShowFlashMessage(true);
        };
    };

    return(
        <div className="column">
            {showFlashMessage && (
                <FlashMessage
                    message={flashMessage}
                    type={flashMessageType}
                    onClose={() => setShowFlashMessage(false)}
                />
            )}
            <form className="box" onSubmit={handleSubmit}>
                <h1 className="title">Register</h1>
                <div className="field">
                    <label className="label">Username</label>
                    <div className="control">
                        <input 
                        type="username" 
                        placeholder="Enter Username" 
                        value={username} 
                        onChange={ (e) => setUsername(e.target.value)}
                        className="input"
                        required
                        />
                    </div>
                </div>
                <div className="field">
                    <label className="label">Email Address</label>
                    <div className="control">
                        <input 
                        type="email" 
                        placeholder="Enter Email" 
                        value={email} 
                        onChange={ (e) => setEmail(e.target.value)}
                        className="input"
                        required
                        />
                    </div>
                </div>
                <div className="field">
                    <label className="label">Password</label>
                    <div className="control">
                        <input 
                        type="password" 
                        placeholder="Enter Password" 
                        value={password} 
                        onChange={ (e) => setPassword(e.target.value)}
                        className="input"
                        required
                        />
                    </div>
                </div>
                <div className="field">
                    <label className="label">Confirm Password</label>
                    <div className="control">
                        <input 
                        type="password" 
                        placeholder="Enter Password" 
                        value={confirmationPassword} 
                        onChange={ (e) => setConfirmationPassword(e.target.value)}
                        className="input"
                        required
                        />
                    </div>
                </div>
                <FlashMessage message={flashMessage}></FlashMessage>
                <br></br>
                <button className="button" type="submit">Register</button>
            </form>
        </div>
    );
};


export default Register