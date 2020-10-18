<template>
  <div class="flex">
    <div class="flex-wrap">
      <h1>Enter Username to see your blog</h1>
      <input
          v-model="username"
          class="item-row-form-input"
          type="text"
          autocomplete="off"
      >
      <button class="btn"
              @click="goToBlog()"
      >
        Login
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: "Login",

  data() {
    return {
      username: '',
      data: []
    }
  },
  methods: {
    goToBlog () {
      axios
        .get('http://localhost:5000/blog/login/' + this.username + '/')
        .then(response => {
          this.data = response.data;
          if (response.status === 200) {
            this.$router.push({path: 'blog/'+response.data.blog_id + '/'})
          }
        })
        .catch(error => console.log(error));
    }
  }
}
</script>

<style>

.flex {
  display: flex;
}

.flex-wrap {
  margin: 0 auto;
  display: flex;
  flex-wrap: wrap;
  flex-direction: column;
}

.item-row-form-input {
  font-size: 1.125rem;
  margin-bottom: 10px;
  outline: none;
  border: none;
  background: white;
  border-bottom: 1px solid black;
  /*color: black;*/
}

.btn {
  margin: 0 auto;
  outline: none;
  border: none;
  background: #36B54F;
  display: flex;
  width: 10rem;
  min-height: 3.5rem;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1.25rem;
  font-family: 'Montserrat Medium', Helvetica, Arial, sans-serif;
}

</style>