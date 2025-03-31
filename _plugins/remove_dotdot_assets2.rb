Jekyll::Hooks.register :documents, :pre_render do |document|
  if document.extname == ".md"
    content = document.content

    # 如果有 Markdown 图片语法并且出现了 '..'
    if content.include?("![") && content.include?("..")
      # 删除路径中的 '..'，保留后面的 '/'
      updated_content = content.gsub(/\!\[([^\]]*)\]\((.*?)\)/) do |match|
        alt_text = Regexp.last_match(1)
        path = Regexp.last_match(2).gsub('..', '')
        "![#{alt_text}](#{path})"
      end

      document.content = updated_content
    end
  end
end
