import Card from "../Layout/Card";
import Activity from "./Activity";

const Activities = (props) => {
  return (
    <>
      {props.showDetails && (
        <Card>
          {props.activities.map((activity) => {
            return <Activity activity={activity}></Activity>;
          })}
        </Card>
      )}
    </>
  );
};
export default Activities;
