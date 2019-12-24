import axios from 'axios'
import { Message } from 'element-ui'


const service = axios.create(({
    // baseURL: 'http://192.168.135.128:7300/mock/5dd6c9eacc546d0b141fb290',
    baseURL: 'http://127.0.0.1:5000/',
    // baseURL: 'https://118.25.153.97/',
    // baseURL: 'http://192.168.31.188:9003',
    timeout: 50000,
}));

service.interceptors.response.use(
    response => {
        return response
    },
    error => {
        Message({
            message: error.message,
            type: 'error'
        })
        return Promise.reject(error)
    }
)
export default service;
