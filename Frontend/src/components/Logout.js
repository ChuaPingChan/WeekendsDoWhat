import Card from "../Layout/Card";
import React, { useState } from "react";
import "./Logout.css";
import { Constants } from "../Utils/Constants";
import { useHistory } from "react-router-dom/cjs/react-router-dom.min";
import { useDispatch } from "react-redux";
import { Redirect } from "react-router-dom";

const Logout = () => {
  const history = useHistory();
  const dispatch = useDispatch();
  localStorage.removeItem("token");
  dispatch({ type: "logout" });
  history.push("/home");
  return <Redirect to='/login'  />
};
export default Logout;
