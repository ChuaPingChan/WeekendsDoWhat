import { Fragment, useState } from "react";
import Card from "../Layout/Card";
import Modal from "../UI/Modal";
import { Constants } from "../Utils/Constants";
import classes from "./Activity.module.css";
import { FaStar } from "react-icons/fa";
import Review from "./Review";

const Activity = (props) => {
  const activity = props.activity;
  const [showActivityDetailsModal, setShowActivityDetailsModal] =
    useState(false);
  const [imageUrl, setImageUrl] = useState("");
  const [placeDetails, setplaceDetails] = useState();
  const [showAddReview, setShowAddReview] = useState(false);

  const isPremium = props.state.isPremium;
  const showActivityDetails = async () => {
    const reader = new FileReader();
    const res = await getImageDetails();
    const imageBlob = await res.blob();
    reader.readAsDataURL(imageBlob);
    reader.onloadend = () => {
      const base64data = reader.result;
      setImageUrl(base64data);
    };
    const placeDetails = await getPlaceDetails();
    setplaceDetails(placeDetails);
    setShowActivityDetailsModal(true);
  };

  const getPlaceDetails = async () => {
    const url = `${Constants.api_endpoint}/place_info?place_id=${activity.id}&place_type=${activity.type}`;
    const res = await fetch(url, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
        "Content-Type": "application/json",
      },
    });
    const data = await res.json();
    return data;
  };

  const getImageDetails = async () => {
    const url = `${Constants.api_endpoint}/place_image?place_id=${activity.id}`;
    const res = await fetch(url, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });
    return res;
  };
  const handleAfterSubmitReview = async () => {
    setShowAddReview(false);
    const placeDetails = await getPlaceDetails();
    setplaceDetails(placeDetails);
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
          <div className={classes.header}>
            <h1 className={classes["header-content"]}>{placeDetails.name}</h1>
          </div>

          {!showAddReview && (
            <div>
              <div
                style={{
                  display: "flex",
                  flexDirection: "row",
                  margin: "10px",
                }}
              >
                <div
                  style={{
                    flexGrow: "2",
                  }}
                >
                  <p>{placeDetails.address}</p>
                  <div
                    style={{
                      display: "flex",
                      flexDirection: "row",
                    }}
                  >
                    <p>{placeDetails.rating.toFixed(1)}</p>
                    <FaStar
                      color="#FFC300"
                      style={{
                        position: "relative",
                        top: "17px",
                        left: "10px",
                      }}
                    ></FaStar>
                  </div>
                </div>
                <div>
                  <img
                    src={imageUrl}
                    style={{
                      width: "200px",
                      height: "200px",
                    }}
                    alt="No Image"
                  ></img>
                </div>
              </div>
              {isPremium && (
                <div>
                  <button type="button" onClick={() => setShowAddReview(true)}>
                    Add a review
                  </button>
                </div>
              )}
              {placeDetails.reviews.length > 0 && (
                <div
                  style={{
                    overflow: "scroll",
                  }}
                >
                  <h3>Reviews:</h3>
                  {placeDetails.reviews.map((review) => {
                    return (
                      <Card>
                        <div
                          style={{
                            display: "flex",
                            flexDirection: "row",
                          }}
                        >
                          <div
                            style={{
                              flexGrow: 2,
                            }}
                          >
                            <p>{review.review}</p>
                          </div>
                          <div
                            style={{
                              display: "flex",
                              flexDirection: "row",
                            }}
                          >
                            <p>{review.rating}</p>
                            <FaStar
                              color="#FFC300"
                              style={{
                                position: "relative",
                                top: "17px",
                                left: "10px",
                              }}
                            ></FaStar>
                          </div>
                        </div>
                      </Card>
                    );
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
