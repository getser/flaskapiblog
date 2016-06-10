  Test project. REST API based FLASK application to keep, add and delete visitor's posts. Temporarily available for testing at: http://getser.*******/


  Description available at "/flaskapiblog/api":
        This is the REST API based FLASK application. Current API version is 1.0.
        Post resouce gives access to "Post" objects and supports described actions.
        Visitor resouce gives access to "Visitor" objects and supports described actions.
        Resource examples are explained using "curl" utility.

      Post actions: 
          add post: "curl -u ss@gov.ua:ss -i -H "Content-Type: application/json" -X POST -d '{"title":"post title","text":"post text"}' http://127.0.0.1:5000/flaskapiblog/api/v1.0/posts", 

          delete post with email/password or token: "curl -u visitor_token:none -i -X DELETE http://127.0.0.1:5000/flaskapiblog/api/v1.0/posts/13",

          find posts: "curl -i -H "Content-Type: application/json" -X POST -d '{"text":"text to be found"}' http://127.0.0.1:5000/flaskapiblog/api/v1.0/posts/find",

          get all posts: "curl -i http://127.0.0.1:5000/flaskapiblog/api/v1.0/posts",

          get all posts paginated with email/password or token": "curl -u visitor_email@gov.ua:visitor_password -i http://127.0.0.1:5000/flaskapiblog/api/v1.0/posts/paginated/<int:page>",

          get post: "curl -i http://127.0.0.1:5000/flaskapiblog/api/v1.0/posts/<int:post_id>",

          get visitors posts with email/password or token: "curl -u visitor_email@gov.ua:visitor_password -i http://127.0.0.1:5000/flaskapiblog/api/v1.0/posts/my_posts", 

      Visitors actions: 
          add visitor: "curl -i -H "Content-Type: application/json" -X POST -d '{"email":"visitors_email@gov.ua","password":"visitors_password"}' http://127.0.0.1:5000/flaskapiblog/api/v1.0/visitors",

          delete visitor with email/password or token": "curl -u visitor_token:none -i -X DELETE http://127.0.0.1:5000/flaskapiblog/api/v1.0/visitors/<int:visitor_id>",

          get all visitors: "curl -i http://127.0.0.1:5000/flaskapiblog/api/v1.0/visitors",

          get profile with email/password or token: "curl -u visitor_email@gov.ua:visitor_password -i http://127.0.0.1:5000/flaskapiblog/api/v1.0/visitors/my_profile",

          get token with email/password only: "curl -u visitor_email@gov.ua:visitor_password -i http://127.0.0.1:5000/flaskapiblog/api/v1.0/token",