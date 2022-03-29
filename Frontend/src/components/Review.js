import React, { useState } from "react";
import classes from "./Review.module.css";
import { FaStar } from "react-icons/fa";
import { Constants } from "../Utils/Constants";

const colors = {
  orange: "#FFBA5A",
  grey: "#a9a9a9",
};

const Review = (props) => {
  const [currentValue, setCurrentValue] = useState(0);
  const [hoverValue, setHoverValue] = useState(undefined);

  const [reviewText, setReviewText] = useState("");
  const stars = Array(5).fill(0);

  const handleClick = (value) => {
    setCurrentValue(value);
  };

  const handleMouseOver = (newHoverValue) => {
    setHoverValue(newHoverValue);
  };

  const handleMouseLeave = () => {
    setHoverValue(undefined);
  };
  const handleSubmitReview = async () => {
    await postSubmitReview();
    props.afterSubmit();
  };
  const postSubmitReview = async () => {
    const url = `${Constants.api_endpoint}/add_review`;
    const body = {
      rating: currentValue,
      review: reviewText,
      place_id: props.placeId,
    };
    const res = fetch(url, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });
    if (!res.ok) {
      return;
    }
    const data = await res.json();
    return data;
  };
  return (
    <>
      <div className={classes.container}>
        <div className={classes.stars}>
          {stars.map((_, index) => {
            return (
              <FaStar
                key={index}
                size={24}
                onClick={() => handleClick(index + 1)}
                onMouseOver={() => handleMouseOver(index + 1)}
                onMouseLeave={handleMouseLeave}
                color={
                  (hoverValue || currentValue) > index
                    ? colors.orange
                    : colors.grey
                }
                style={{
                  marginRight: 10,
                  cursor: "pointer",
                }}
              />
            );
          })}
        </div>
        <textarea
          placeholder="Write a review"
          className={classes.textarea}
          onChange={(e) => setReviewText(e.target.value)}
        />

        <div>
          <button
            type="button"
            onClick={handleSubmitReview}
            className={classes.submitReview}
          >
            Submit
          </button>
          <button
            type="button"
            onClick={() => props.afterSubmit()}
            className={classes.submitReview}
          >
            Cancel
          </button>
        </div>
      </div>
    </>
  );
};
export default Review;
