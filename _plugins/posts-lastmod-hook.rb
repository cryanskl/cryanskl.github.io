#!/usr/bin/env ruby
#
# 多功能文章处理器：
# 1. 记录文章最后修改时间

Jekyll::Hooks.register :posts, :post_init do |post|
  # 功能1：保留原有的最后修改时间记录
  commit_num = `git rev-list --count HEAD "#{post.path}"`
  if commit_num.to_i > 1
    lastmod_date = `git log -1 --pretty="%ad" --date=iso "#{post.path}"`
    post.data['last_modified_at'] = lastmod_date
  end
end
