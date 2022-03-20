import { useState } from "react";
import Card from "../Layout/Card";
import { Constants } from "../Utils/Constants";
import { useHistory } from "react-router-dom";
const Signup = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [username, setUsername] = useState("");
  const history = useHistory()

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await fetch(`${Constants.api_endpoint}/signup`, {
      method: "POST",
      body: JSON.stringify({
        email: email,
        password: password,
        username: username,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (!res) {
      history.push("/login");
      return;
    }
    const data = await res.json();
    localStorage.setItem("token", data.access_token);
    history.push("/home");
  };
  return (
    <div className="Login">
      <Card>
        <form
          style={{
            margin: "20px 25px 0px 0px",
          }}
        >
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
              type="username"
              required="required"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <span>Username</span>
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
            <input type="button" value="Sign Up" onClick={handleSubmit} />
          </div>
        </form>
      </Card>
    </div>
  );
};
export default Signup;
