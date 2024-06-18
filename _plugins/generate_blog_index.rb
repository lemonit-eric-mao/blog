module Jekyll
  class BlogIndexGenerator < Generator
    safe true

    def generate(site)
      years = {}
      
      site.posts.docs.each do |post|
        year = post.date.strftime("%Y")
        years[year] ||= []
        years[year] << post
      end

      site.data['years'] = years
    end
  end
end
