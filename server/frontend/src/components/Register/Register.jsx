import React, { useState } from 'react';
import './Register.css';

const Register = () => {
    const [userName, setUserName] = useState("");
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const register = async (e) => {
        e.preventDefault();
        // Registration endpoint logic
        console.log({ userName, firstName, lastName, email, password });
        alert("Registration logic triggered!");
    };

    return (
        <div className="register_container">
            <h2>Sign Up</h2>
            <form onSubmit={register}>
                <div className="input_field">
                    <label>Username</label>
                    <input 
                        type="text" 
                        name="username" 
                        placeholder="Enter Username" 
                        value={userName} 
                        onChange={(e) => setUserName(e.target.value)} 
                        required 
                    />
                </div>
                <div className="input_field">
                    <label>First Name</label>
                    <input 
                        type="text" 
                        name="firstname" 
                        placeholder="Enter First Name" 
                        value={firstName} 
                        onChange={(e) => setFirstName(e.target.value)} 
                        required 
                    />
                </div>
                <div className="input_field">
                    <label>Last Name</label>
                    <input 
                        type="text" 
                        name="lastname" 
                        placeholder="Enter Last Name" 
                        value={lastName} 
                        onChange={(e) => setLastName(e.target.value)} 
                        required 
                    />
                </div>
                <div className="input_field">
                    <label>Email</label>
                    <input 
                        type="email" 
                        name="email" 
                        placeholder="Enter Email" 
                        value={email} 
                        onChange={(e) => setEmail(e.target.value)} 
                        required 
                    />
                </div>
                <div className="input_field">
                    <label>Password</label>
                    <input 
                        type="password" 
                        name="password" 
                        placeholder="Enter Password" 
                        value={password} 
                        onChange={(e) => setPassword(e.target.value)} 
                        required 
                    />
                </div>
                <button type="submit" className="register_btn">Register</button>
            </form>
        </div>
    );
};

export default Register;