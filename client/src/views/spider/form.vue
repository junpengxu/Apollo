<template>
  <div class="form">
    <el-form ref="form" :model="form" :rules="rules" label-width="120px">
      <el-form-item prop="desc" label="任务描述">
        <el-input v-model="form.desc" />
      </el-form-item>
      <el-form-item prop="topic_id" label="贴吧帖子id">
        <el-input v-model.number="form.topic_id" autocomplete="off" />
      </el-form-item>
      <el-form-item
        label="开始页码"
        prop="start_page"
      >
        <el-input v-model.number="form.start_page" autocomplete="off" />
      </el-form-item>
      <el-form-item
        label="结束页码"
        prop="end_page"
      >
        <el-input v-model.number="form.end_page" autocomplete="off" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm('form')">创建任务</el-button>
        <el-button>取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>
<script>
import { createSpiderTask } from '@/api/spider'

export default {
  data() {
    return {
      form: {
        topic_id: '',
        start_page: '',
        end_page: '',
        desc: ''
      },
      rules: {
        topic_id: [
          { required: true, message: '帖子id不能为空' },
          { type: 'number', message: '帖子id必须为数字值' }
        ],
        start_page: [
          { required: true, message: '结束页码不能为空' },
          { type: 'number', message: '页码必须为数字值' }
        ],
        end_page: [
          { required: true, message: '结束页码不能为空' },
          { type: 'number', message: '页码必须为数字值' }
        ]
      }
    }
  },
  methods: {

    submitForm(form) {
      this.$refs[form].validate((valid) => {
        if (valid) {
          const params = {
            'topic_id': this.form.topic_id,
            'desc': this.form.desc,
            'start_page': this.form.start_page,
            'end_page': this.form.end_page
          }
          createSpiderTask(params).then(response => {
            const h = this.$createElement
            this.$notify({
              title: '任务创建成功',
              message: h('i', { style: 'color: teal' }, '爬虫任务创建成功'),
              duration: 8000
            })
            this.$router.push({ path: '/spider/list', query: {}})
          }).catch(err => {
            console.log(err)
          })
        } else {
          console.log('error submit')
        }
      })
    }
  }
}
</script>

<style scoped>
  .form{
    width: 60%;
    margin: 50px;
  }
</style>

