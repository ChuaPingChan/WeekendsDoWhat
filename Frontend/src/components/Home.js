import React, { useEffect, useState } from "react";
import { useHistory } from "react-router-dom/cjs/react-router-dom.min";
import Select from "react-select";
import Modal from "../UI/Modal";
import { Constants } from "../Utils/Constants";
import classes from "./Home.module.css";

const Home = (props) => {
  const [locations, setLocations] = useState([]);
  const [location, setLocation] = useState({
    label: "",
    value: "",
  });
  const history = useHistory();
  // const [isPremium, setIsPremium] = useState(false);
  const [showModal, setShowModal] = useState(true);

  const isPremium = props.isPremium;

  if (!props.state.isLoggedIn) {
    history.push("/login");
  }

  useEffect(async () => {
    const res = await fetch(`${Constants.api_endpoint}/all_districts`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
        "Content-Type": "application/json",
      },
    });
    if (res) {
      const data = await res.json();
      setLocations(
        data.districts.map((loc) => {
          return {
            value: loc,
            label: loc,
          };
        })
      );
    } else {
      history.push("/login");
    }
  }, []);
  const handleSearch = () => {
    history.push(`/itineraries/${location.value}`);
  };
  const handleChangeInput = (e) => {
    setLocation({
      label: e.label,
      value: e.value,
    });
  };
  const setUserToPremium = async () => {
    const res = await fetch(`${Constants.api_endpoint}/set_premium_user`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
        "Content-Type": "application/json",
      },
    });
    if (res) {
      // const data = await res.json();
      setShowModal(false);
    }
  };
  return (
    <React.Fragment>
      {!isPremium && showModal && (
        <Modal onClose={() => setShowModal(false)}>
          <div className={classes.text}>
            <span
              style={{
                fontSize: "30px",
                fontWeight: "bold",
              }}
            >
              Do you want to be a premium user?
            </span>
          </div>
          <div className={classes.actions}>
            <button
              className={classes["button--alt"]}
              onClick={setUserToPremium}
            >
              Yes
            </button>
            <button
              className={classes["button--alt"]}
              onClick={() => setShowModal(false)}
            >
              No
            </button>
          </div>
        </Modal>
      )}
      <div
        style={{
          position: "absolute",
          top: "200px",
          width: "400px",
          left: "550px",
        }}
      >
        <h1
          style={{
            color: "white",
          }}
        >
          Where do you want to go?
        </h1>
        <Select options={locations} onChange={handleChangeInput}></Select>
        <div
          style={{
            display: "flex",
            justifyContent: "center",
          }}
        >
          <button
            className={classes.searchButton}
            type="button"
            onClick={handleSearch}
          >
            Search
          </button>
        </div>
      </div>
      {/* <div className="App">
        {!showList && (
          <div>
            <Input ref={inputLoc}></Input>
            <button onClick={showListHandler}>Search</button>
          </div>
        )}
        
      </div> */}
    </React.Fragment>
  );
};
export default Home;
