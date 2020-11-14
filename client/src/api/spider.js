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

export function searchTiebaTaskSesult(data) {
  return request({
    url: '/spider/search_tieba_task_result',
    method: 'post',
    data
  })
}

