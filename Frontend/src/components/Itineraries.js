import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { useHistory } from "react-router-dom/cjs/react-router-dom.min";
import Card from "../Layout/Card";
import { Constants } from "../Utils/Constants";
import Activities from "./Activities";
const Itineraries = () => {
  const [locationList, setLocationList] = useState([]);
  const [showDetails, setShowDetails] = useState(false);
  const params = useParams();
  const history = useHistory();
  useEffect(async () => {
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
    <>
      {locationList.map((loc, index) => {
        return (
          <Card>
            <ul key={loc.id}>
              <li>
                <div>
                  <h1>Itinerary {index + 1}</h1>
                  <span>{loc.activities.length} activities</span>
                </div>
                <div>
                  <button type="button" onClick={() => setShowDetails(true)}>
                    Details
                  </button>
                </div>
                <Activities
                  activities={loc.activities}
                  showDetails={showDetails}
                ></Activities>
              </li>
            </ul>
          </Card>
        );
      })}
    </>
  );
};
export default Itineraries;
