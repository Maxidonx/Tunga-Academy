from flask import Flask
from flask import url_for
from flask import request
from flask import render_template
from flask import redirect
from flask import jsonify


app = Flask(__name__)

# In-memory storage for blog posts
posts = []

@app.route('/', methods=['GET'])
def index():
    return 'Home Page'

@app.route('/about', methods=['GET'])
def about():
    return 'This is an about page'

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
def post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        return f"Post Created! <br> Title: {title} <br> Content: {content}"

    return '''
        <form method="post">
            <label>Title:</label>
            <input type="text" name="title"><br>
            <label>Content:</label>
            <textarea name="content"></textarea><br>
            <button type="submit">Submit</button>
        </form>
    '''
@app.route('/update-post/<int:post_id>', methods=['GET', 'PUT'])
def update_post(post_id):
    if post_id not in posts:
        return "Post not found!", 404

    if request.method == 'PUT':
        title = request.form.get('title')
        content = request.form.get('content')
        posts[post_id] = {'title': title, 'content': content}
        return redirect(url_for('index'))

    return f'''
        <h2>Update Post</h2>
        <form method="post" onsubmit="updatePost(event, {post_id})">
            <label>Title:</label>
            <input type="text" name="title" value="{posts[post_id]['title']}" required><br>
            <label>Content:</label>
            <textarea name="content" required>{posts[post_id]['content']}</textarea><br>
            <button type="submit">Update</button>
        </form>
        <br>
        <a href="/">Back to Home</a>
    '''


@app.route('/delete-post/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    if post_id in posts:
        del posts[post_id]
        return redirect(url_for('index'))
    return "Post not found!", 404



if __name__ == '__main__':
    app.run(debug=True)