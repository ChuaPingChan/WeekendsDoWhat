import React from "react";
import Loader from "./../assets/Loader.gif";
import classes from "./Spinner.module.css";
const Spinner = () => {
  return (
    <div className={classes.container}>
      <img className={classes.loader} src={Loader} alt="Loading"></img>
      {/* <div className={classes["sk-chase"]}>
        <div className={classes["sk-chase-dot"]}></div>
        <div className={classes["sk-chase-dot"]}></div>
        <div className={classes["sk-chase-dot"]}></div>
        <div className={classes["sk-chase-dot"]}></div>
        <div className={classes["sk-chase-dot"]}></div>
        <div className={classes["sk-chase-dot"]}></div>
      </div> */}
    </div>
  );
};
export default Spinner;
