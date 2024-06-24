require 'json'

module Jekyll
  class JsonGenerator < Generator
    safe true

    def generate(site)
      data = site.posts.docs.map do |post|
        {
          title: post.data['title'],
          date: post.data['date'],
          url: post.url,
          content: post.content
        }
      end

      File.open(File.join(site.dest, 'index.json'), 'w') do |f|
        f.write(JSON.pretty_generate(data))
      end
    end
  end
end
