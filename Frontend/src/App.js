import logo from "./logo.svg";
import "./App.css";
import { useRef, useState } from "react";
import Card from "./Layout/Card";
import Input from "./Layout/Input";

const locations = [
  {
    key: 0,
    name: "Clementi Woods Park",
    location: "Clementi",
    restaurant: "Old Chang Kee",
  },
  {
    key: 1,
    name: "Clementi Woods Park",
    location: "Clementi",
    restaurant: "Seizeria",
  },
  {
    key: 2,
    name: "Clementi Woods Park",
    location: "Clementi",
    restaurant: "Properous Kitchen",
  },
  {
    key: 3,
    name: "One North",
    location: "Buona Vista",
    restaurant: "Old Chang Kee",
  },
  {
    key: 3,
    name: "Kent Ridge Park",
    location: "Buona Vista",
    restaurant: "Old Chang Kee",
  },
];
// const ITINERARIES = [
//   {
//     activities: [
//       {
//         type: "food",
//         name: "COLD STORAGE",
//         address: "301 C, Block 3, TEMASEK BOULEVARD",
//       },
//       {
//         type: "park",
//         name: "Lilac Drive Playground",
//         address: "...",
//       },
//       {
//         type: "food",
//         name: "THE SOUP SPOON",
//         address: "8 MARINA VIEW",
//       },
//     ],
//   },
//   {
//     activities: [
//       {
//         type: "food",
//         name: "TAO SEAFOOD ASIA",
//         address: "12 MARINA VIEW",
//       },
//       {
//         type: "park",
//         name: "MacRitchie Reservoir Park",
//         address: "123 Lornie Road",
//       },
//       {
//         type: "food",
//         name: "THE SOUP SPOON",
//         address: "8 MARINA VIEW",
//       },
//     ],
//   },
// ];
function App() {
  const [showList, setShowList] = useState(false);
  const inputLoc = useRef();
  const [locationList, setLocationList] = useState([]);
  const showListHandler = async () => {
    const inputLocation = inputLoc.current.value;
    const response = await fetch(
      `http://192.168.1.204:5000/getitinerary?location=${inputLocation}`
    );
    const responseData = await response.json();
    const itineraries = responseData.itineraries.map((itin) => {
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
    setShowList(true);
    setLocationList(itineraries);
  };
  return (
    <div className="App">
      {!showList && (
        <div>
          <Input ref={inputLoc}></Input>
          <button onClick={showListHandler}>Search</button>
        </div>
      )}
      {showList &&
        locationList.map((loc) => {
          return (
            <Card>
              <ul>
                <li>
                  <div>
                    {/* <h3>{loc.name}</h3>
                    <div>{loc.restaurant}</div>
                    <div>{loc.location}</div> */}
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
    </div>
  );
}

export default App;
