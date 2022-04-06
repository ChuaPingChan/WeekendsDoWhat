import React from "react";
import classes from "./Header.module.css";
import { NavLink } from "react-router-dom";
import logo from '../logo-white.png'

const LoginLogoutSignup = (props) => {
  if (!props.state.isLoggedIn) {
    return  <nav>
              <ul>
                <li>
                  <NavLink activeClassName={classes.active} to="/login">
                    Login
                  </NavLink>
                </li>
                <li>
                  <NavLink activeClassName={classes.active} to="/signup">
                    Signup
                  </NavLink>
                </li>
              </ul>
            </nav>;
  } else {
    return  <nav>
              <ul>
                <li>
                  <NavLink activeClassName={classes.active} to="#">
                    Feedback
                  </NavLink>
                </li>
                <li>
                  <NavLink activeClassName={classes.active} to="/logout">
                    Logout
                  </NavLink>
                </li>
              </ul>
            </nav>;
  }
}

const Header = (props) => {
  return (
    <React.Fragment>
      <header className={classes.header}>
        <img
          src={logo}
          className="d-inline-block align-top"
        />
        <a href="/home">
        <h1
          style={{
            marginLeft: "50px",
          }}
        >
          WeekendsDoWhat
        </h1>
        </a>
        <LoginLogoutSignup state={props.state}></LoginLogoutSignup>
      </header>
    </React.Fragment>
  );
};
export default Header;
