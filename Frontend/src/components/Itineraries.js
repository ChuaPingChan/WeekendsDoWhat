import React, { Fragment, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { useHistory } from "react-router-dom/cjs/react-router-dom.min";
import useFullPageSpinner from "../hooks/useFullPageSpinner";
import Card from "../Layout/Card";
import { Constants } from "../Utils/Constants";
import Activities from "./Activities";
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
      {locationList.map((loc, index) => {
        return (
          <Card>
            <ul>
              <li key={loc.id}>
                <div>
                  <h1>Itinerary {index + 1}</h1>
                  <span>{loc.activities.length} activities</span>
                </div>
                <Activities activities={loc.activities} state={props.state}></Activities>
              </li>
            </ul>
          </Card>
        );
      })}
    </Fragment>
  );
};
export default Itineraries;
