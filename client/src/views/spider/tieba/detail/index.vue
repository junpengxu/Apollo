<template>
  <div class="app-container">
    <el-table
      :data="tableData"
    >
      <el-table-column
        prop="post_id"
        label="帖子id"
        width="160"
      />
      <el-table-column
        prop="content"
        label="帖子内容"
      />
      <el-table-column
        prop="user_id"
        label="发帖用户"
        width="160"
      />
      <el-table-column
        prop="publish_time"
        label="发帖时间"
        width="260"
      />
      <el-table-column
        prop="floor_id"
        label="楼层"
        width="80"
      />
    </el-table>
    <div class="block" style="float: right">
      <el-pagination
        :current-page="this.page"
        :page-sizes="[10, 50, 100, 200]"
        :page-size="this.offset"
        layout="total, sizes, prev, pager, next, jumper"
        :total="this.totalNum"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script>
import { searchTiebaTaskSesult } from '@/api/spider'

export default {
  data() {
    return {
      page: 1,
      offset: 100,
      totalNum: 1000,
      tableData: [],
      topic_id: ''
    }
  },
  created() {
    this.topic_id = this.$route.query.topic_id
    this.filter()
  },
  methods: {
    filter() {
      const params = {
        topic_id: this.topic_id,
        page: this.page,
        offset: this.offset
      }
      searchTiebaTaskSesult(params).then(response => {
        const h = this.$createElement
        this.$notify({
          title: '搜索成功',
          message: h('i', { style: 'color: teal' }, '搜索成功'),
          duration: 1000
        })
        this.tableData = response.data['post_info']
        this.totalNum = response.data['total_nums']
      }).catch(err => {
        console.log(err)
      })
    },
    handleSizeChange(val) {
      this.offset = val
    },
    handleCurrentChange(val) {
      this.page = val
      this.filter()
    }
  }
}
</script>
