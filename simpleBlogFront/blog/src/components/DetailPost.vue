<template>
  <div>
    <h3 class="content_text">Title: {{ post.title }}</h3>
    <p class="content_text">Content: {{ post.content }}</p>
    <p>created date: {{ data_created }}</p>
  </div>
</template>

<script>
import axios from "axios";

const HOST_URL = 'http://localhost:5000'

export default {
  name: "DetailPost",

  created() {
    this.getPostDetail()
  },

  data() {
    return {
      post_id: this.$route.params.post_id,
      post: {}
    }
  },

  computed: {
    data_created () {
      let date = this.post.date_created.replace(/:\d{2}\.\d+Z$/, '');
      return date
    }
  },

  methods: {
    getPostDetail() {
      axios
          .get(HOST_URL + '/blog/post/' + this.post_id + '/',)
          .then(response => {
            this.post = response.data
          })
          .catch(error => console.log(error));
    }
  }
}
</script>

<style scoped>

</style>