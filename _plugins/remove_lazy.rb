# _plugins/remove_lazy.rb
Jekyll::Hooks.register [:pages, :documents], :post_render do |doc|
    doc.output = doc.output.gsub('loading="lazy"', '')
  end
  