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
function App() {
  const [showList, setShowList] = useState(false);
  const inputLoc = useRef();
  const [locationList, setLocationList] = useState(locations);
  const showListHandler = () => {
    const inputLocation = inputLoc.current.value;
    setShowList(true);
    setLocationList(locations.filter((loc) => inputLocation === loc.location));
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
                    <h3>{loc.name}</h3>
                    <div>{loc.restaurant}</div>
                    <div>{loc.location}</div>
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
