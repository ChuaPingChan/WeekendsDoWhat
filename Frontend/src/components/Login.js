import Card from "../Layout/Card";
import React, { useState } from "react";
import "./Login.css";
import { Constants } from "../Utils/Constants";
import { useHistory } from "react-router-dom/cjs/react-router-dom.min";

const Login = (props) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorStatus, setErrorStatus] = useState(false);
  const history = useHistory();

  const handleLogin = async (e) => {
    e.preventDefault();
    const res = await fetch(`${Constants.api_endpoint}/login`, {
      method: "POST",
      body: JSON.stringify({
        email: email,
        password: password,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (!res.ok) {
      setErrorStatus(true);
      return;
    }
    if (res) {
      setErrorStatus(false);
      const data = await res.json();
      localStorage.setItem("token", data.access_token);
      props.handleUserLogin(data.is_premium);
      history.push("/home");
    }
  };

  return (
    <div className="Login">
      <Card>
        <form
          style={{
            margin: "20px 25px 0px 0px",
          }}
        >
          {errorStatus && (
            <p
              style={{
                color: "red",
                marginBottom: "30px",
              }}
            >
              Incorrect email or password
            </p>
          )}
          <div className="inputbox">
            <input
              type="email"
              required="required"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <span>Email</span>
          </div>
          <div className="inputbox">
            <input
              type="password"
              required="required"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <span>Password</span>
          </div>
          <div className="inputbox">
            <input type="button" value="Login" onClick={handleLogin} />
          </div>
        </form>
      </Card>
    </div>
  );
};
export default Login;
