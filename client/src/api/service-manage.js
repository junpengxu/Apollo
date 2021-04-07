import request from '@/utils/request'

export function getAllServerNode(data) {
  return request({
    url: '/service_manage/get_all_service',
    method: 'post',
    data
  })
}
