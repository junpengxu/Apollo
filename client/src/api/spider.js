import request from '@/utils/request'

export function createSpiderTask(data) {
  return request({
    url: '/spider/create_task',
    method: 'post',
    data
  })
}
export function searchSpiderTask(data) {
  return request({
    url: '/spider/search_task',
    method: 'post',
    data
  })
}

