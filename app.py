from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return "Flask Proxy is Running! Use /proxy/{URL} to access a website."

@app.route('/proxy/<path:url>', methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def proxy(url):
    try:
        # Ensure the URL starts with http/https
        if not url.startswith("http"):
            url = "http://" + url

        headers = {key: value for key, value in request.headers if key.lower() not in ["host", "content-length"]}

        # Forward the request to the actual URL
        if request.method == "GET":
            resp = requests.get(url, headers=headers, params=request.args, verify=False)
        elif request.method == "POST":
            resp = requests.post(url, headers=headers, json=request.get_json(), data=request.data, verify=False)
        elif request.method == "DELETE":
            resp = requests.delete(url, headers=headers, verify=False)
        elif request.method == "PUT":
            resp = requests.put(url, headers=headers, json=request.get_json(), data=request.data, verify=False)
        elif request.method == "PATCH":
            resp = requests.patch(url, headers=headers, json=request.get_json(), data=request.data, verify=False)
        else:
            return Response("Method Not Allowed", status=405)

        # Remove unnecessary headers
        excluded_headers = ["content-encoding", "content-length", "transfer-encoding", "connection"]
        response_headers = [(name, value) for (name, value) in resp.headers.items() if name.lower() not in excluded_headers]

        return Response(resp.content, resp.status_code, response_headers)

    except requests.exceptions.RequestException as e:
        return Response(f"Request failed: {str(e)}", status=500)

if __name__ == "__main__":
    app.run(debug=True, port=80)
