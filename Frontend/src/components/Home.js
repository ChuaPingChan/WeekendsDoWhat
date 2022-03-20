import React, { useEffect, useState } from "react";
import { useHistory } from "react-router-dom/cjs/react-router-dom.min";
import Select from "react-select";
import { Constants } from "../Utils/Constants";
import classes from "./Home.module.css";

const Home = () => {
  const [locations, setLocations] = useState([]);
  const [location, setLocation] = useState({
    label: "",
    value: "",
  });
  const history = useHistory();
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
  return (
    <>
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
        <div>
          <button className={classes.search} type="text" onClick={handleSearch}>
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
    </>
  );
};
export default Home;
