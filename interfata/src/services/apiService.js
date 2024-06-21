import axios from 'axios';
import { getToken, getUserId } from '../composables/tokenManagement';

const api = axios.create({
  baseURL: 'http://localhost:5000',
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(config => {
  const { token } = getToken();
  config.headers['x-access-token'] = token.value;
  return config;
});

export const getUserFromDB = async () => {
  const url = `/user/${getUserId()}`;
  const response = await api.get(url);
  return response.data;
};

export const postRequest = async (url, requestBody) => {
  const response = await api.post(url, requestBody);
  return response.data;
};
export const putRequest = async (url, requestBody) => {
  const response = await api.put(url, requestBody);
  return response.data;
};

export const getCSV = async (url, requestBody) => {
  const response = await api.post(url, requestBody, { responseType: 'blob' });
  return response.data;
};

export const updatePub = async (requestBody) => {
  const url = `/publications/${requestBody.publicationId}`;
  return await putRequest(url, requestBody);
};

export const splitPublication = async (pubId) => {
  const url = `/publications/${pubId}/split`;
  return await postRequest(url, {});
};
