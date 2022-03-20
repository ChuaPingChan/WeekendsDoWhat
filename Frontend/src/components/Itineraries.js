import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { useHistory } from "react-router-dom/cjs/react-router-dom.min";
import Card from "../Layout/Card";
import { Constants } from "../Utils/Constants";
const Itineraries = () => {
  const [locationList, setLocationList] = useState([]);
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
              id: Math.random(),
              type: activity.type,
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
      {locationList.map((loc) => {
        return (
          <Card>
            <ul>
              <li>
                <div>
                  <h3>{loc.name}</h3>
                  <div>{loc.restaurant}</div>
                  <div>{loc.location}</div>
                  {loc.activities.map((activity) => {
                    return (
                      <ul>
                        <li>
                          <div>
                            <h3>{activity.type}</h3>
                            <div>{activity.name}</div>
                            <div>{activity.address}</div>
                          </div>
                        </li>
                      </ul>
                    );
                  })}
                </div>
              </li>
            </ul>
          </Card>
        );
      })}
    </>
  );
};
export default Itineraries;
