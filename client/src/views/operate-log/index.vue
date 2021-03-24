<template>
  <div>

    <div class="app-container">
      <div>
        <el-input v-model="input" class="input-content" placeholder="请输入搜索内容" />
        <el-button class="search-button" type="primary" @click="onSubmit">搜索</el-button>
      </div>
      <el-table
        :data="tableData"
      >
        <el-table-column
          prop="executor"
          label="执行人"
        />
        <el-table-column
          prop="action"
          label="行为"
        />
        <el-table-column
          prop="remote_ip"
          label="ip地址"
        />
        <el-table-column
          prop="create_time"
          label="操作时间"
        />
        <el-table-column
          prop="params"
          label="请求参数"
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
  </div>
</template>

<script>
import { searchOperateLog } from '@/api/operate-log'

export default {
  name: 'OperateLogVue',
  data() {
    return {
      page: 1,
      offset: 10,
      totalNum: 1000,
      tableData: [],
      input: ''
    }
  },
  created() {
    this.filter()
  },
  methods: {
    filter() {
      const params = {
        page: this.page,
        offset: this.offset,
        content: this.input
      }
      searchOperateLog(params).then(response => {
        const h = this.$createElement
        this.tableData = response.data.data
        this.totalNum = response.data['total_nums']
        this.$notify({
          title: '搜索成功',
          message: h('i', { style: 'color: teal' }, '搜索成功'),
          duration: 1000
        })
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
    },
    onSubmit() {
      this.tableData = []
      this.filter()
    }
  }
}
</script>

<style scoped>
.input-content {
  width: 500px;
}
.search-button {
  margin-left: 100px;
}
</style>
