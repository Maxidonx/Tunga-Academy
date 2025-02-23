from flask import Flask, url_for, request, redirect, jsonify

app = Flask(__name__)

# In-memory storage for blog posts
posts = []

@app.route('/', methods=['GET'])
def index():
    return 'Home Page - <a href="{}">Create Post</a>'.format(url_for('create_post'))

@app.route('/about', methods=['GET'])
def about():
    return 'This is an about page'

# Returns a JSON response
@app.route('/api/data', methods=['GET'])
def get_data():
    data = {
        "message": "Welcome to my Blog",
        "status": "success",
        "items": [
            {"id": 1, "name": "Tunga"},
            {"id": 2, "name": "Assignment"}
        ]
    }
    return jsonify(data)

@app.route('/create-post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            title = data.get("title")
            content = data.get("content")
        else:
            title = request.form.get("title")
            content = request.form.get("content")

        if not title or not content:
            return jsonify({"error": "Missing title or content"}), 400

        new_post = {
            "id": len(posts) + 1,
            "title": title,
            "content": content
        }
        posts.append(new_post)
        return jsonify({"message": "Post created!", "post": new_post}), 201

    return '''
    <form method="post" action="/create-post">
        Title: <input type="text" name="title"><br>
        Content: <textarea name="content"></textarea><br>
        <input type="submit" value="Create Post">
    </form>
    '''


@app.route('/update-post/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    for post in posts:
        if post["id"] == post_id:
            post["title"] = data.get("title", post["title"])
            post["content"] = data.get("content", post["content"])
            return jsonify({"message": "Post updated!", "post": post}), 200

    return jsonify({"error": "Post not found"}), 404


@app.route('/delete-post/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    global posts
    posts = [post for post in posts if post["id"] != post_id]
    return jsonify({"message": "Post deleted!"})

if __name__ == '__main__':
    app.run(debug=True)
