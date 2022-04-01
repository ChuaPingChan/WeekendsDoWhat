import { Fragment, useState } from "react";
import Card from "../Layout/Card";
import Activity from "./Activity";
import classes from "./Activities.module.css";

const Activities = (props) => {
  const [showDetails, setShowDetails] = useState(false);
  return (
    <Fragment>
      <div
        style={{
          marginBottom: "20px",
        }}
      >
        <button
          className={classes.details}
          type="button"
          onClick={() =>
            setShowDetails((prev) => {
              return !prev;
            })
          }
        >
          {!showDetails ? "Show Details" : "Hide Details"}
        </button>
      </div>
      {showDetails && (
        <Card>
          {props.activities.map((activity) => {
            return <Activity activity={activity} state={props.state}></Activity>;
          })}
        </Card>
      )}
    </Fragment>
  );
};
export default Activities;
