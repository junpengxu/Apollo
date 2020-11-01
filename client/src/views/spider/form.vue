<template>
  <div class="form">
    <el-form ref="form" :model="form" :rules="rules" label-width="120px">
      <el-form-item prop="desc" label="任务描述">
        <el-input v-model="form.desc" />
      </el-form-item>
      、      <el-form-item prop="url" label="贴吧链接">
        <el-input v-model="form.url" />
      </el-form-item>
      <el-form-item prop="headers" label="请求头信息">
        <el-input v-model="form.headers" type="textarea" :rows="10" />
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
        url: '',
        headers: '',
        start_page: '',
        end_page: '',
        desc: ''
      },
      rules: {
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
            'url': this.form.url,
            'desc': this.form.desc,
            'headers': this.form.headers,
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

