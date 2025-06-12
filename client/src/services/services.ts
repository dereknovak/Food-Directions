import axios from 'axios';

const BASE_URL = 'http://localhost:3000/api';

export const getRestaurants = async (question) => {
  const { data } = await axios.post(`${BASE_URL}/ask`, question);
  return data;
};
