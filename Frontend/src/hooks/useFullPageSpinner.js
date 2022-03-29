import { useState } from "react";
import Spinner from "../UI/Spinner";

const useFullPageSpinner = () => {
  const [loading, setLoading] = useState(false);
  return [
    loading ? <Spinner></Spinner> : null,
    () => setLoading(true), // Show spinner
    () => setLoading(false), // Hide spinner
  ];
};
export default useFullPageSpinner;
