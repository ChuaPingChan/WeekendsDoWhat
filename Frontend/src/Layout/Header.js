import React from "react";
import classes from "./Header.module.css";
import bgImage from "../assets/background_image.jpg";
import { NavLink } from "react-router-dom";
const Header = () => {
  return (
    <React.Fragment>
      <header className={classes.header}>
        <h1
          style={{
            marginLeft: "50px",
          }}
        >
          WeekendsDoWhat
        </h1>
        <nav>
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
        </nav>
      </header>
    </React.Fragment>
  );
};
export default Header;
