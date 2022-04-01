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

  const isPremium = props.state.isPremium;

  if (!localStorage.getItem("token")) {
    history.push("/login");
  }

  useEffect(async () => {
    const res = await fetch(`${Constants.api_endpoint}/all_districts`, {
      method: "GET"
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
          top: "50%",
          width: "400px",
          left: "50%",
          transform: "translate(-50%, -50%)"
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

      {/* <div>
        <div className="ad">
          <script data-num-rows="3" src="https://s3-us-west-2.amazonaws.com/kaboodle/kaboodle.js" type="text/javascript"></script>
          <div class="kaboodle-module">
            <a class="kaboodle-header" href="https://github.com/ptsteadman/kaboodle">Sponsored Links By Kaboodle</a>
            <div class="kaboodle-items">
              <a href="http://www.fool.com/video-alert/stock-advisor/sa-nightmare-gfx/">
                <div class="kaboodle-item">
                  <img src="https://s3-us-west-2.amazonaws.com/kaboodle/creatives/buffet.jpg" />
                  <p>4 in 5 Americans Are Ignoring Buffet's Warning</p>
                </div>
              </a>
              <a href="http://elitedaily.com/life/satisfied-people-dont-wait-want-go-get">
                <div class="kaboodle-item">
                  <img src="https://s3-us-west-2.amazonaws.com/kaboodle/creatives/genius.jpg" />
                  <p>10 Tips To Learn Any Language From The Genius Who Speaks 9</p>
                </div>
              </a>
              <a href="http://elitedaily.com/humor/who-is-this-text-most-insulting-text-video/">
                <div class="kaboodle-item">
                  <img src="https://s3-us-west-2.amazonaws.com/kaboodle/creatives/whois.jpg" />
                  <p>Why 'Who Is This?' Is Literally The Most Insulting Test Ever (Video)</p>
                </div>
              </a>
            </div>
          </div>
        </div>
      </div> */}
    </React.Fragment>
  );
};
export default Home;
