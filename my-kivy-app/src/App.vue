<template>
  <div id="app">
    <nav class="sidebar">
      <ul class="nav-list">
        <li><router-link to="/" class="nav-link">首页</router-link></li>
        <li><router-link to="/file-selection" class="nav-link">选择文件</router-link></li>
        <li><router-link to="/feature-extraction" class="nav-link">特征向量提取</router-link></li>
        <li><router-link to="/image-stitching" class="nav-link">图像拼接</router-link></li>
        <li><router-link to="/region-selection" class="nav-link">区域选择</router-link></li>
      </ul>
    </nav>
    <main>
      <router-view/>
    </main>
  </div>
</template>

<style>
#app {
  display: flex;
  min-height: 100vh; /* 设置页面高度为视口高度 */
}

.sidebar {
  width: 200px;
  background-color: #f9f9f9;
  padding: 20px;
  box-sizing: border-box;
  flex-grow: 1; /* 让导航栏占据剩余的空间 */
}

.nav-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.nav-link {
  display: block;
  padding: 10px;
  text-decoration: none;
  color: #2c3e50;
}

.nav-link:hover {
  background-color: #f2f2f2;
}

.router-link-active {
  color: #42b983;
}
</style>
