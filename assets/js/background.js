window.addEventListener('load', function () {
  // 检查背景图像是否已存储
  if (!localStorage.getItem('sidebar-background-loaded')) {
    // 如果没有设置过，设置背景图像并标记为已加载
    localStorage.setItem('sidebar-background-loaded', 'true');
    document.querySelector('#sidebar').style.backgroundImage =
      "url('/assets/img/tom.jpeg')";
  }
});
