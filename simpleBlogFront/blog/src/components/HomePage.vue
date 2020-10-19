<template>
  <div class="flex">
    <div class="header">

      <button class="btn" @click="MyBlogChecker = !MyBlogChecker">My blog</button>
      <button class="btn" @click="FollowChecker = !FollowChecker">Follow someone</button>
      <button class="btn" @click="LookPostsChecker= !LookPostsChecker">Look followed posts</button>

    </div>

<!--    BLOCK WITH FORM FOR CREATING POSTS AND LIST OF SELF POSTS-->
    <div v-if="MyBlogChecker">
      <div class="flex-wrap form-wrap width_50">

        <input
            placeholder="Title"
            v-model="title"
            class="item-row-form-input"
            type="text"
            autocomplete="off"
        >
        <textarea
            placeholder="Content Text"
            name="Content"
            id="Content_text"
            cols="30" rows="10"
            v-model="content_text">
        </textarea>
        <button class="btn" @click="createPost()">Create</button>

      </div>
      <h2>My Posts</h2>
      <div class="flex-wrap width_50 blogs" v-for="(post, key) in posts" :key="key">
        <div>

          <h3 class="content_text">Title: {{ post.title }}</h3>
          <p class="content_text">Content: {{ post.content }}</p>
          <p class="content_text">created date: {{ dateFormat(post.date_created) }}</p>

        </div>
        <div class="mg-left_auto">
          <button class="btn delete_button" @click="deletePost(post.id)" >Delete</button>
        </div>
      </div>
    </div>
<!--    BLOCK WITH USERS BLOGS LIST -->
    <div v-if="FollowChecker">
      <h2>My Follows</h2>
      <div class="flex-wrap width_50 blogs" v-for="(blog, key) in users_blogs" :key="key">

        <h3> {{ blog.username }} Blog </h3>
        <input class="checkbox mg-left_auto"
               type="checkbox"
               v-model="blog.checker"
               @click="followBlogAction(blog.id)">

      </div>
    </div>
<!--    BLOCK WITH FOLLOW BLOG POSTS-->
    <div v-if="LookPostsChecker">

      <h3 v-if="!follow_posts.length">Here is nothing to Look</h3>
      <h3 v-if="follow_posts.length">Follow Blog Posts</h3>
      <h3 v-if="follow_posts.length" class="status-header">Read/Unread</h3>

      <div class="flex-wrap width_50 blogs" v-for="(post, key) in follow_posts" :key="key">
        <div @click="postDetails(post.id)">

          <h3 class="content_text">Title: {{ post.title }}</h3>
          <p class="content_text">Content: {{ post.content }}</p>
          <p class="content_text">created date: {{ dateFormat(post.date_created) }}</p>

        </div>
        <div class="mg-left_auto">
          <input class="checkbox mg-left_auto"
               type="checkbox"
               v-model="post.checker"
               @click="readPostAction(post.id)">
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

const HOST_URL = 'http://localhost:5000'

export default {
  name: "HomePage",

  created() {
    this.getUser()
    this.getBlogPosts(this.blog_id)
  },

  watch: {
    LookPostsChecker() {
      if (this.LookPostsChecker) {
        this.FollowChecker = false
        this.MyBlogChecker = false
      }
    },
    FollowChecker() {
      if (this.FollowChecker) {
        this.MyBlogChecker = false
        this.LookPostsChecker = false
      }
    },
    MyBlogChecker() {
      if (this.MyBlogChecker) {
        this.FollowChecker = false
        this.LookPostsChecker = false
      }
    }
  },
  data() {
    return {
      LookPostsChecker: false,
      FollowChecker: false,
      MyBlogChecker: true,
      title: '',
      content_text: '',
      posts: [],
      follow_posts: [],
      blog_id: this.$route.params.blog_id,
      user_id: '',
      users_blogs: [],
      user: {},
    }
  },

  computed: {

    form_data() {
      return {title: this.title, content: this.content_text, blog_id: this.blog_id}
    },

    follow_blogs () {
        if (this.user.followed_blogs) {
          return this.user.followed_blogs
        } else return  0
    }
  },

  methods: {

    dateFormat (date) {
      return date.replace(/:\d{2}\.\d+Z$/, '');
    },

    postDetails (post_id) {
      this.$router.push({path: '/post/'+ post_id + '/'})
    },

    deletePost (post_id) {
      axios
          .delete(HOST_URL + '/blog/post/'+ post_id +'/')
          .then(response => {
            if (response.status === 204) {
              let itemIndex = this.posts.findIndex(item => item.id === post_id);
              this.posts.splice(itemIndex, 1);
            }
          })
          .catch(error => console.log(error));
    },

    followBlogAction (blog_id) {
      axios
          .put(HOST_URL + '/blog/user_blog/' + blog_id + '/', {user_id: this.user.id},)
          .then(() => this.getUser())
          .catch(error => console.log(error));
    },

    readPostAction (post_id) {
      axios
          .put(HOST_URL + '/blog/post/' + post_id + '/', {user_id: this.user.id},)
          .catch(error => console.log(error));
    },

    getUsersBlogs() {
      axios
          .get(HOST_URL + '/blog/user_blog/', {params: {blog_id: this.blog_id}},)
          .then(response => {
            this.users_blogs = response.data.map(item => {
              if (item.blog_followers_ids.includes(this.user.id)) {
                item.checker = true;
                return item
              } else item.checker = false;
              return item
            })
          })
          .catch(error => console.log(error));
    },

    getUser() {
      return axios.get(HOST_URL + '/blog/user/' + this.blog_id + '/')
          .then(response => {
            this.user = response.data
            this.getBlogPosts(this.follow_blogs, true)
            this.getUsersBlogs()
          })
          .catch(error => console.log(error));
    },

    createPost() {
      axios
          .post(HOST_URL + '/blog/post/', this.form_data)
          .then(response => {
            if (response.status === 201) {
              this.posts.unshift(response.data)
              this.title = ''
              this.content_text = ''
            }
          })
          .catch(error => console.log(error));
    },

    getBlogPosts(blog_id, followers) {
      axios
          .get(HOST_URL + '/blog/post/', {params: {blog_id: blog_id}})
          .then(response => {
            if (followers) {
              this.follow_posts = response.data.map(item => {
                if (item.users_read_ids.includes(this.user.id)) {
                  item.checker = true;
                  return item
                } else item.checker = false;
                return item
              })
            } else this.posts = response.data
          })
          .catch(error => console.log(error));

    }
  }
}
</script>

<style scoped>
.status-header {
  text-align: right;
  width: 90%
}
.mg-left_auto {
  margin-left: auto;
}

.content_text {
  text-align: left;
  padding: 0 1rem;
}
.form-wrap {
  padding-bottom: 10px;
  border-bottom: 1px solid green;
}
.delete_button {
  background: red;
  width: 4rem;
}
.blogs {
  flex-wrap:nowrap;
  border-bottom: 1px solid green;
  flex-direction: row;
  align-items: center;
}

.header {
  margin: 0 auto;
  display: flex;
  border-radius: 5px;
  width: 80%;
  height: 4rem;
  padding: 3rem;
}

.width_50 {
  width: 70%;
}

.btn {
  margin-top: 20px;
}

.flex {
  flex-direction: column;
  padding: 30px;
  height: 40rem;
}
</style>