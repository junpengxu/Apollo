import request from '@/utils/request'

export function zongyue(data) {
  return request({
    url: '/spider/zongyue',
    method: 'post',
    data
  })
}
