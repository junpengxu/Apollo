<template>
  <div class="app-container">
    <div>
      <el-input v-model="content" style="width: 60%" placeholder="根据帖子内容搜索" />
      <el-button style="margin-left: 20px" type="primary" @click="filter">提交</el-button>
    </div>
    <el-table
      :data="tableData"
    >
      <el-table-column
        prop="content"
        label="帖子内容"
      />
      <el-table-column
        label="发帖用户"
        width="100"
      >
        <template v-slot="scope">
          {{ scope._self.userInfo[scope.row.user_id]["nickname"] || scope._self.userInfo[scope.row.user_id]["user_name"]
          }}
        </template>
      </el-table-column>
      <el-table-column
        label="用户头像"
        width="80"
      >
        <template v-slot="scope">
          <el-image :src="scope.row.avatar" />
        </template>
      </el-table-column>
      <el-table-column
        prop="publish_time"
        label="发帖时间"
        width="240"
      />
      <el-table-column
        label="贴吧页面"
        width="100"
      >
        <template v-slot="scope">
          <a :href="scope.row.topic_url" target="_blank">
            <el-link type="primary" target="_blank">点击跳转</el-link>
          </a>
        </template>
      </el-table-column>
      <el-table-column
        prop="page"
        label="页号"
        width="80"
      />
      <el-table-column
        prop="floor_id"
        label="楼层"
        width="80"
      />
      <el-table-column
        type="expand"
        label="展开回复"
        width="100"
      >
        <template v-slot="scope" v-bind="replyInfo">
          <el-table :data="replyInfo[scope.row.post_id]">
            <el-table-column
              prop="content"
              label="content"
            />
            <el-table-column
              prop="reply_time"
              label="回复时间"
              width="200"
            />
            <el-table-column
              label="用户名"
              width="100"
            >
              <template v-slot="scope">
                {{ scope._self.userInfo[scope.row.user_id]["nickname"] || scope._self.userInfo[scope.row.user_id]["user_name"] }}
              </template>
            </el-table-column>
            <el-table-column
              label="用户头像"
              width="100"
            >
              <template v-slot="scope">
                <el-image :src="scope._self.userInfo[scope.row.user_id]['avatar']" />
              </template>
            </el-table-column>
          </el-table>
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
import { searchTiebaTaskSesult } from '@/api/spider'

export default {
  data() {
    return {
      page: 1,
      offset: 100,
      totalNum: 1000,
      tableData: [],
      topic_id: '',
      userInfo: {},
      replyInfo: {},
      content: ''
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
        offset: this.offset,
        content: this.content
      }
      searchTiebaTaskSesult(params).then(response => {
        const h = this.$createElement
        this.$notify({
          title: '搜索成功',
          message: h('i', { style: 'color: teal' }, '搜索成功'),
          duration: 1000
        })
        this.tableData = response.data['post_info']
        this.userInfo = response.data['user_info']
        this.replyInfo = response.data['reply_info']
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
