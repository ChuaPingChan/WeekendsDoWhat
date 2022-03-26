import React, { Fragment } from "react";
import reactDom from "react-dom";
import classes from "./Modal.module.css";

const Backdrop = (props) => {
  return <div className={classes.backdrop} onClick={props.onClose}></div>;
};
const ModalOverlay = (props) => {
  return (
    <div className={classes.modal}>
      <div className={classes.content}>{props.children}</div>
    </div>
  );
};
const Modal = (props) => {
  const overlayElement = document.getElementById("overlays");
  return (
    <Fragment>
      {reactDom.createPortal(
        <Backdrop onClose={props.onClose}></Backdrop>,
        overlayElement
      )}
      {reactDom.createPortal(
        <ModalOverlay>{props.children}</ModalOverlay>,
        overlayElement
      )}
    </Fragment>
  );
};
export default Modal;
