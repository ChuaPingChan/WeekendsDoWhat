import React, { Fragment, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { useHistory } from "react-router-dom/cjs/react-router-dom.min";
import useFullPageSpinner from "../hooks/useFullPageSpinner";
import Card from "../Layout/Card";
import { Constants } from "../Utils/Constants";
import Activities from "./Activities";
import classes from "./Itineraries.module.css";

// Images for fake ads
import buffet from "../assets/buffet.jpg";
import genius from "../assets/genius.jpg";
import whois from "../assets/whois.jpg";

const Itineraries = (props) => {
  const [locationList, setLocationList] = useState([]);

  const [loader, showSpinner, hideSpinner] = useFullPageSpinner();
  const params = useParams();
  const history = useHistory();
  useEffect(async () => {
    showSpinner();
    const res = await fetch(
      `${Constants.api_endpoint}/get_itineraries?location=${params.location}&num_itineraries=4`,
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
          "Content-Type": "application/json",
        },
      }
    );
    if (!res) {
      history.push("/login");
    } else {
      hideSpinner();
      const data = await res.json();
      const itineraries = data.itineraries.map((itin) => {
        return {
          id: Math.random(),
          activities: itin.activities.map((activity) => {
            return {
              id: activity.place_id,
              type: activity.place_type,
              name: activity.name,
              address: activity.address,
            };
          }),
        };
      });
      setLocationList(itineraries);
    }
  }, []);
  return (
    <Fragment>
      {loader}
      <div>
      {locationList.map((loc, index) => {
        return (
          <Card>
            <ul>
              <li key={loc.id}>
                <div>
                  <h1>Itinerary {index + 1}</h1>
                  {/* <span>{loc.activities.length} activities</span> */}
                </div>
                <Activities activities={loc.activities} state={props.state}></Activities>
              </li>
            </ul>
          </Card>
        );
      })}
      </div>

      {/* Fake ads */}
      <div className={classes.ads}>
        <div>
          <script data-num-rows="3" src="https://s3-us-west-2.amazonaws.com/ads/ads.js" type="text/javascript"></script>
          <div className={classes.adsModule}>
            <div className="adsItems">
              {/* <a href="http://www.fool.com/video-alert/stock-advisor/sa-nightmare-gfx/"> */}
              <div className={classes.adsItem}>
                  <img src={buffet} />
                  <p>4 in 5 Americans Are Ignoring Buffet's Warning</p>
                </div>
              {/* </a> */}
              {/* <a href="http://elitedaily.com/life/satisfied-people-dont-wait-want-go-get"> */}
                <div className={classes.adsItem}>
                  <img src={genius} />
                  <p>10 Tips To Learn Any Language From The Genius Who Speaks 9</p>
                </div>
              {/* </a> */}
              {/* <a href="http://elitedaily.com/humor/who-is-this-text-most-insulting-text-video/"> */}
              <div className={classes.adsItem}>
                  <img src={whois} />
                  <p>Why 'Who Is This?' Is Literally The Most Insulting Test Ever (Video)</p>
                </div>
              {/* </a> */}
            </div>
          </div>
        </div>
      </div>
    </Fragment>
  );
};
export default Itineraries;
