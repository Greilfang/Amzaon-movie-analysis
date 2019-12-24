import request from '~/utils/request'

const API_NAME = "api";
export default {
  getRelations(searchMap){
    return request({
      url: `/${API_NAME}/query_relations`,
      method: 'POST',
      data: searchMap
    })
  }
}
