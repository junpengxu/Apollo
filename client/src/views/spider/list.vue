<template>
  <div class="app-container">
    <el-table
      :data="tableData"
    >
      <el-table-column
        prop="id"
        label="ID"
        width="80"
      />
      <el-table-column
        prop="desc"
        label="任务描述"
        width="400"
      />
      <el-table-column
        prop="topic_id"
        label="帖子id"
      />      <el-table-column
        prop="start_page"
        label="开始页码"
      />
      <el-table-column
        prop="end_page"
        label="结束页码"
      />
      <el-table-column
        fixed="right"
        label="操作"
        width="100"
      >
        <template slot-scope="scope">
          <el-button type="text" size="small" @click="handleClick(scope.row)">查看结果</el-button>
        </template>
      </el-table-column>
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
import { searchSpiderTask } from '@/api/spider'

export default {
  data() {
    return {
      page: 1,
      offset: 10,
      totalNum: 1000,
      tableData: []
    }
  },
  created() {
    this.filter()
  },
  methods: {
    filter() {
      const params = {
        page: this.page,
        offset: this.offset
      }
      searchSpiderTask(params).then(response => {
        const h = this.$createElement
        this.$notify({
          title: '搜索成功',
          message: h('i', { style: 'color: teal' }, '搜索成功'),
          duration: 1000
        })
        this.tableData = response.data.data
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
