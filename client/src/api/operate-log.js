import request from '@/utils/request'

export function searchOperateLog(data) {
  return request({
    url: '/operate_log/search',
    method: 'post',
    data
  })
}
