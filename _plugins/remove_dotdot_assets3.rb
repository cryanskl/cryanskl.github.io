Jekyll::Hooks.register :site, :post_render do |page|
    # 确保只对 Markdown 文件进行处理
    if page.is_a?(Jekyll::Document) && page.extname == '.md'
      # 读取当前 Markdown 文件的内容
      content = page.content
  
      # 只在文件中包含图片语法时进行处理
      if content.include?("![") && content.include?("../")
        # 替换路径，将 '../assets' 改为 '/assets'
        updated_content = content.gsub(/\!\[([^\]]*)\]\(\.\.\/assets\//, '![\1](/assets/')
  
        # 更新页面内容
        page.content = updated_content
      end
    end
  end
  