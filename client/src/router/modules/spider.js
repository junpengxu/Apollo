/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const spiderRouter =
  {
    redirect: '/spider/tieba/form',
    path: '/spider',
    component: Layout,
    name: '爬虫',
    meta: {
      title: '爬虫',
      icon: 'el-icon-s-help'
    },
    children: [{
      path: 'tieba',
      component: () => import('@/views/spider/tieba/index'),
      name: 'tieba',
      meta: { title: '百度贴吧', icon: 'documentation' },
      children: [
        {
          path: 'form',
          component: () => import('@/views/spider/tieba/form/index'),
          name: '爬虫任务页面',
          meta: { title: '爬虫任务创建', icon: 'documentation' }
        },
        {
          path: 'list',
          component: () => import('@/views/spider/tieba/list/index'),
          name: '爬虫任务列表',
          meta: { title: '爬虫任务列表', icon: 'documentation' }
        },
        {
          path: 'detail',
          hidden: true,
          component: () => import('@/views/spider/tieba/detail/index'),
          name: '任务详情页',
          meta: { title: '任务详情页', icon: 'documentation' }
        }
      ]
    }]
  }

export default spiderRouter
