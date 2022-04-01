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

class App extends React.Component {
  constructor () {
    super();
    this.state = {
      isPremium: false,
      isLoggedIn: false
    }

    this.handleUserLogin = this.handleUserLogin.bind(this);
  }

  handleUserLogin = (isPremiumOrNot) => {
    this.setState({
      isPremium: isPremiumOrNot,
      isLoggedIn: true
    })
  }

  handleUserLogout = () => {
    this.setState({
      isPremium: false,
      isLoggedIn: false
    })
  }

  render () {
    return (
      <React.Fragment>
        <div>
          <Header state={this.state}></Header>
        </div>
        <div>
          <Switch>
            <Route path="/" exact>
              <Redirect to="/login"></Redirect>
            </Route>
            <Route path="/login">
              <Login handleUserLogin={this.handleUserLogin}></Login>
            </Route>
            <Route path="/logout">
              <Logout handleUserLogout={this.handleUserLogout}></Logout>
            </Route>
            <Route path="/signup">
              <Signup></Signup>
            </Route>
            <Route path="/home" exact>
              <Home state={this.state}></Home>
            </Route>
            <Route path="/itineraries/:location">
              <Itineraries></Itineraries>
            </Route>
          </Switch>
        </div>
      </React.Fragment>
    );
  }
}

export default App;
