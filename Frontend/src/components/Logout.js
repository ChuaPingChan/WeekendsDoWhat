import React, { useState } from "react";
import { useHistory } from "react-router-dom/cjs/react-router-dom.min";
import { Redirect } from "react-router-dom";

const Logout = (props) => {
  const history = useHistory();
  localStorage.removeItem("token");
  props.handleUserLogout();
  history.push("/home");
  return <Redirect to='/login'  />
};
export default Logout;
