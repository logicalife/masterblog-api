from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def get_post_by_postid(id):
    """ Accepts int:id as a parameter and returns post for thag ID"""
    for post in POSTS:
        if post['id'] == id:
            return post


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    """ This function returns the sorted List of posts"""
    if request.method == 'GET':
        sort = request.args.get('sort')
        direction = request.args.get('direction')
        if sort == 'title':
            if direction == 'asc':
                return jsonify(sorted(POSTS, key=lambda x: x['title']))
            if direction == 'dec':
                return jsonify(sorted(POSTS, key=lambda x: x['title'], reverse=True))
            else:
                return jsonify("Invalid querry parameter")
        if sort == 'content':
            if direction == 'asc':
                return jsonify(sorted(POSTS, key=lambda x: x['content']))
            if direction == 'dec':
                return jsonify(sorted(POSTS, key=lambda x: x['content'], reverse=True))
            else:
                return jsonify("Invalid querry parameter")
        return jsonify(POSTS)
    if request.method == 'POST':
        data = request.json
        if data['title'] == "" or data['content'] == "":
            return jsonify(f'Missing field(s):{[x for x in data if data[x] == ""]}'), 400
        id = max([post['id'] for post in POSTS]) + 1
        POSTS.append({'id': id, 'title': data['title'], 'content': data['content']})
        return jsonify(POSTS), 201


@app.route('/api/posts/<int:id>', methods=['DELETE', 'PUT'])
def manage_post(id):
    """This function manages (Delete and Update) existing posts and returns new list of posts"""
    post = get_post_by_postid(id)
    if post == None:
        return jsonify(f'There is no post with the post id:{id}'), 404
    if request.method == 'DELETE':
        POSTS.remove(post)
        return jsonify({"message": f"Post with id {post['id']} has been deleted successfully."}), 200
    if request.method == 'PUT':
        new_post = request.json
        if "title" in new_post:
            post['title'] = new_post['title']
        if "content" in new_post:
            post['content'] = new_post['content']
        return jsonify({"id": f"{post['id']}", "title": f"{post['title']}", "content": f"{post['content']}"}), 200


@app.route('/api/posts/search', methods=['GET'])
def search_post():
    """ This function returns search result based in query string"""
    title_str = request.args.get('title').casefold()
    content_str = request.args.get('content')
    result_posts = []
    for post in POSTS:
        if title_str in post['title'].casefold() or content_str in post['content'].casefold():
            result_posts.append(post)
    return jsonify(result_posts), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
