<template>
  <div>

    <div class="app-container">

      <el-table
        :data="tableData"
      >
        <el-table-column
          prop="node_name"
          label="节点名称"
        />
        <el-table-column
          prop="node_host"
          label="节点ip"
        />
        <el-table-column
          prop="node_port"
          label="节点端口"
        />
        <el-table-column
          prop="node_register_time"
          label="注册时间"
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
import { getAllServerNode } from '@/api/service-manage'

export default {
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
      getAllServerNode(params).then(response => {
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
