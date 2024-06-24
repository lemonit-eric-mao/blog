require 'json'

module Jekyll
  class JsonGenerator < Generator
    safe true

    def generate(site)
      posts = site.posts.docs.map do |post|
        {
          title: post.data['title'],
          date: post.data['date'].to_s,
          url: post.url,
          content: post.content
        }
      end

      File.open(File.join(site.dest, 'index.json'), 'w') do |file|
        file.write(JSON.pretty_generate(posts))
      end
    end
  end
end
