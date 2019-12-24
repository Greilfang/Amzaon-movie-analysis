import request from '~/utils/request'

const API_NAME = 'api';
export default {
  getDetailList(searchMap){
    return request({
      url: `/${API_NAME}/query_movie_details`,
      method: 'POST',
      data: searchMap
    })
  },
  getBriefList(searchMap){
    return request({
      url: `/${API_NAME}/query_movie_list`,
      method: 'POST',
      data: searchMap
    })
  }
}
