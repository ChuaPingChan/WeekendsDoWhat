import "./App.css";
import React from "react";
import Header from "./Layout/Header";
import { Route } from "react-router-dom";
import Login from "./components/Login";
import Logout from "./components/Logout";
import Signup from "./components/Signup";
import Home from "./components/Home";
import { Switch } from "react-router-dom";
import { Redirect } from "react-router-dom";
import Itineraries from "./components/Itineraries";

function App() {
  return (
    <React.Fragment>
      <div>
        <Header></Header>
      </div>
      <div>
        <Switch>
          <Route path="/" exact>
            <Redirect to="/login"></Redirect>
          </Route>
          <Route path="/login">
            <Login></Login>
          </Route>
          <Route path="/logout">
            <Logout></Logout>
          </Route>
          <Route path="/signup">
            <Signup></Signup>
          </Route>
          <Route path="/home" exact>
            <Home></Home>
          </Route>
          <Route path="/itineraries/:location">
            <Itineraries></Itineraries>
          </Route>
        </Switch>
      </div>
    </React.Fragment>
  );
}

export default App;
