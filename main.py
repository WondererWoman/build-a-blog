#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import webapp2
import jinja2


from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class BlogEntry(db.Model):
    title = db.StringProperty(required = True)
    blog_entry = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class Blog(Handler):
    def render_blog(self, title="", blog_entry=""):
        blogs = db.GqlQuery("SELECT * FROM BlogEntry "
                            "ORDER BY created DESC "
                            "LIMIT 5")
        self.render("blog.html", title=title, blog_entry=blog_entry, blogs=blogs)

    def get(self):
        self.render_blog()

class MainHandler(Handler):
    def render_base(self, title="", blog_entry="", error=""):
        self.render("base.html", title=title, blog_entry=blog_entry, error=error)

    def get(self):
        self.render_base()

    def post(self):
        title = self.request.get("title")
        blog_entry = self.request.get("blog_entry")

        if title and blog_entry:
            b = BlogEntry(title = title, blog_entry = blog_entry)
            b.put()

            self.redirect('/blog')
        else:
            error = "Please enter a Title and Blog Post!"
            self.render_base(title, blog_entry, error)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/blog', Blog)
], debug=True)
