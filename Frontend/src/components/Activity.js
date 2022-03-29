import { Fragment, useState } from "react";
import Card from "../Layout/Card";
import Modal from "../UI/Modal";
import { Constants } from "../Utils/Constants";
import classes from "./Activity.module.css";
import { FaStar } from "react-icons/fa";
import { useSelector } from "react-redux";
import Review from "./Review";

const Activity = (props) => {
  const activity = props.activity;
  const [showActivityDetailsModal, setShowActivityDetailsModal] =
    useState(false);
  const [imageUrl, setImageUrl] = useState("");
  const [placeDetails, setplaceDetails] = useState();
  const [showAddReview, setShowAddReview] = useState(false);

  const isPremium = useSelector((state) => {
    return state.isPremium;
  });
  const showActivityDetails = async () => {
    const res = await getImageDetails();
    const imageBlob = await res.blob();
    var encodedResponse = btoa(imageBlob);

    // var img = new Image();
    // var container = document.getElementById("newImg");
    const url = "data:image/jpeg;base64," + encodedResponse;
    setImageUrl(url);
    // const imageBlob = await res.blob();
    // const imageObjectURL = URL.createObjectURL(imageBlob);
    // setImageUrl(imageObjectURL);
    const placeDetails = await getPlaceDetails();
    setplaceDetails(placeDetails);
    setShowActivityDetailsModal(true);
  };

  const getPlaceDetails = async () => {
    const url = `${Constants.api_endpoint}/place_info?place_id=${activity.id}&place_type=${activity.type}`;
    const res = await fetch(url);
    const data = await res.json();
    return data;
  };

  const getImageDetails = async () => {
    const url = `${Constants.api_endpoint}/place_image?place_id=${activity.id}`;
    const res = await fetch(url, {});
    return res;
  };
  const handleAfterSubmitReview = () => {
    setShowAddReview(false);
  };
  return (
    <Fragment>
      <Card handleClick={showActivityDetails}>
        <ul>
          <li key={activity.id}>
            <div>
              <h3>{activity.type}</h3>
              <div>{activity.name}</div>
            </div>
          </li>
        </ul>
      </Card>
      {showActivityDetailsModal && (
        <Modal>
          {/* <img src={imageUrl}></img> */}
          <div className={classes.header}>
            <h1 className={classes["header-content"]}>{placeDetails.name}</h1>
          </div>
          {!showAddReview && (
            <div>
              <p>{placeDetails.address}</p>
              <div>
                <p>{placeDetails.rating}</p>
                <FaStar color="#FFC300"></FaStar>
              </div>
              {isPremium && (
                <div>
                  <button type="button" onClick={() => setShowAddReview(true)}>
                    Add a review
                  </button>
                </div>
              )}
              {placeDetails.reviews.length > 0 && (
                <div>
                  <h3>Reviews:</h3>
                  {placeDetails.reviews.map((review) => {
                    return <Card></Card>;
                  })}
                </div>
              )}
              <div
                style={{
                  display: "flex",
                  justifyContent: "center",
                }}
              >
                <button
                  type="button"
                  onClick={() => setShowActivityDetailsModal(false)}
                >
                  Close
                </button>
              </div>
            </div>
          )}
          {showAddReview && (
            <Review
              placeId={activity.id}
              afterSubmit={handleAfterSubmitReview}
            ></Review>
          )}
        </Modal>
      )}
    </Fragment>
  );
};
export default Activity;
