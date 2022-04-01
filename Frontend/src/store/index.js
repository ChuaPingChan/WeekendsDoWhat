import { createStore } from "redux";
const reducer = (state = { isPremium: false }, action) => {
  if(action.type === 'setPremiumUserState'){
    state = {
      isPremium: action.isPremium,
    };
  }
  return state;
};
const store = createStore(reducer);
export default store;
