import { createStore } from "redux";
export const reducer = (state = { isPremium: false, isLoggedIn: false }, action) => {
  if (action.type === 'setPremiumUserState') {
    state = {
      isPremium: action.isPremium,
      isLoggedIn: true
    };
  } else if (action.type === 'logout') {
    state = {
      isPremium: false,
      isLoggedIn: false
    }
  }
  return state;
};
const store = createStore(reducer);
export default store;
