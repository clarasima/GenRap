import { ref } from 'vue';
import {jwtDecode} from 'jwt-decode';

const token = ref(null);
const userId = ref(null);

const removeToken = () => {
  localStorage.removeItem('auth_token');
  token.value = null;
  userId.value = null;
};

const setUserId = (id) => {
  userId.value = id;
};

const getUserId = () => {
  return userId.value;
};

export function isTokenValid(token) {
  if (!token) {
    return false;
  }

  try {
    const decodedToken = jwtDecode(token);
    const currentTime = Date.now() / 1000; // Current time in seconds
    return decodedToken.exp > currentTime;
  } catch (error) {
    console.error('Invalid token:', error);
    return false;
  }
}

const setToken = (newToken) => {
  try {
    if (isTokenValid(newToken)) {
      localStorage.setItem('auth_token', newToken);
      token.value = newToken;
      setUserId(jwtDecode(newToken)._id);
    } else {
      throw new Error('token not valid');
    }
  } catch (err) {
    console.error('error setting', err);
  }
};

try {
  const savedToken = localStorage.getItem('auth_token');
  if (savedToken) {
    setToken(savedToken);
  }
} catch (err) {
  console.error('error initializing', err);
}

const getToken = () => {
  if (isTokenValid(token.value) || !token.value) {
    return { token };
  } else if (token.value) {
    removeToken();
    return null;
  }
};



export { getToken, setToken, removeToken, getUserId };
