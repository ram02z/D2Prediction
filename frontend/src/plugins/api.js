import axios from 'axios';

const devUrl = 'http://localhost:5000/api';
// const prodUrl = 'placeholder';

export default axios.create({
  baseURL: devUrl,
});
